"""
Unit tests for the GCP Billing Budget Kill-Switch (scripts/gcp_budget_killswitch.py).
"""

import base64
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

_SCRIPTS_ROOT = str(Path(__file__).resolve().parent.parent / "scripts")
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

import gcp_budget_killswitch as killswitch  # noqa: E402


def _make_pubsub_event(data_dict: dict) -> dict:
    encoded = base64.b64encode(json.dumps(data_dict).encode("utf-8")).decode("utf-8")
    return {"message": {"data": encoded}}


def test_parse_pubsub_message_valid():
    sample = {"costAmount": 1500.0, "budgetAmount": 2000.0, "currencyCode": "INR"}
    event = _make_pubsub_event(sample)
    payload, err = killswitch.parse_pubsub_message(event)
    assert err is None
    assert payload == sample


def test_parse_pubsub_message_direct_data():
    sample = {"costAmount": 2200.0, "budgetAmount": 2000.0}
    encoded = base64.b64encode(json.dumps(sample).encode("utf-8")).decode("utf-8")
    payload, err = killswitch.parse_pubsub_message({"data": encoded})
    assert err is None
    assert payload == sample


def test_parse_pubsub_message_malformed():
    payload, err = killswitch.parse_pubsub_message({"message": {"data": "not-valid-base64-%%%"}})
    assert err is not None
    assert payload == {}

    payload, err = killswitch.parse_pubsub_message({})
    assert err is not None


def test_check_budget_breach_under_budget():
    payload = {"costAmount": 1200.0, "budgetAmount": 2000.0, "currencyCode": "INR"}
    breached, cost, budget, curr = killswitch.check_budget_breach(payload)
    assert not breached
    assert cost == 1200.0
    assert budget == 2000.0
    assert curr == "INR"


def test_check_budget_breach_at_threshold():
    payload = {"costAmount": 2000.0, "budgetAmount": 2000.0, "currencyCode": "INR"}
    breached, cost, budget, curr = killswitch.check_budget_breach(payload)
    assert breached
    assert cost == 2000.0


def test_check_budget_breach_over_budget():
    payload = {"costAmount": 2450.50, "budgetAmount": 2000.0, "currencyCode": "INR"}
    breached, cost, budget, curr = killswitch.check_budget_breach(payload)
    assert breached
    assert cost == 2450.50


def test_check_budget_breach_missing_or_zero_budget():
    payload = {"costAmount": 100.0, "budgetAmount": 0.0}
    breached, cost, budget, curr = killswitch.check_budget_breach(payload)
    assert not breached


def test_disable_cloud_run_service_dry_run():
    res = killswitch.disable_cloud_run_service(
        project_id="test-proj",
        region="asia-south1",
        service_name="test-service",
        dry_run=True,
    )
    assert res["status"] == "dry_run_success"
    assert res["service_name"] == "test-service"


def test_disable_cloud_run_service_no_token():
    # When no token can be retrieved from metadata server
    with patch("urllib.request.urlopen", side_effect=Exception("Metadata server down")):
        res = killswitch.disable_cloud_run_service(
            project_id="test-proj",
            region="asia-south1",
            service_name="test-service",
            dry_run=False,
            access_token=None,
        )
        assert res["status"] == "error"
        assert "No Google access token" in res["error"]


def test_disable_cloud_run_service_mock_api_success():
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"name": "projects/test-proj/services/test-service"}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = killswitch.disable_cloud_run_service(
            project_id="test-proj",
            region="asia-south1",
            service_name="test-service",
            dry_run=False,
            access_token="test-bearer-token-12345",
        )
        assert res["status"] == "success"
        assert "response" in res


def test_handle_budget_notification_under_budget(monkeypatch):
    monkeypatch.setenv("DRY_RUN", "true")
    event = _make_pubsub_event({"costAmount": 850.0, "budgetAmount": 2000.0, "currencyCode": "INR"})
    res = killswitch.handle_budget_notification(event)
    assert res["status"] == "ok"
    assert res["action"] == "none"
    assert res["cost"] == 850.0


def test_handle_budget_notification_breach(monkeypatch):
    monkeypatch.setenv("DRY_RUN", "true")
    event = _make_pubsub_event({"costAmount": 2050.0, "budgetAmount": 2000.0, "currencyCode": "INR"})
    res = killswitch.handle_budget_notification(event)
    assert res["status"] == "dry_run_success"
    assert res["cost"] == 2050.0
    assert res["budget"] == 2000.0
