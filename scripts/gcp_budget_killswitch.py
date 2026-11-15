#!/usr/bin/env python3
"""
GCP Billing Budget Kill-Switch Cloud Function for LabelFit India.

Subscribes to Google Cloud Pub/Sub budget notification topic.
When cost reaches or exceeds the threshold budgetAmount (e.g. 100% of INR 2000),
it immediately disables Cloud Run multimodal analysis by setting
LABELFIT_ENABLE_ANALYSIS=false and scaling max instances to 0.

Environment Variables:
  GCP_PROJECT_ID: Google Cloud Project ID (e.g. labelfit-india)
  CLOUD_RUN_SERVICE: Service name (e.g. labelfit-backend)
  CLOUD_RUN_REGION: Region (e.g. asia-south1)
  DRY_RUN: 'true' to log actions without mutating GCP resources
"""

import base64
import json
import logging
import os
import sys
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("gcp_budget_killswitch")


def parse_pubsub_message(event: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Extract and decode JSON payload from Cloud Billing Pub/Sub event.
    Returns (payload_dict, error_message).
    """
    if not isinstance(event, dict):
        return {}, "Event is not a dictionary"

    message = event.get("message")
    if not message or not isinstance(message, dict):
        # Handle direct data payload for local testing
        raw_data = event.get("data")
    else:
        raw_data = message.get("data")

    if not raw_data:
        return {}, "Missing 'data' field in Pub/Sub message"

    try:
        decoded_bytes = base64.b64decode(raw_data)
        decoded_str = decoded_bytes.decode("utf-8")
        payload = json.loads(decoded_str)
        return payload, None
    except Exception as exc:
        return {}, f"Failed to decode Pub/Sub data: {exc}"


def check_budget_breach(payload: Dict[str, Any]) -> Tuple[bool, float, float, str]:
    """
    Evaluates whether cost has reached or exceeded budget.
    Returns (is_breached, cost_amount, budget_amount, currency_code).
    """
    cost_amount = float(payload.get("costAmount", 0.0))
    budget_amount = float(payload.get("budgetAmount", 0.0))
    currency_code = str(payload.get("currencyCode", "INR"))

    if budget_amount <= 0.0:
        logger.warning("Budget amount is zero or missing in payload: %s", payload)
        return False, cost_amount, budget_amount, currency_code

    is_breached = cost_amount >= budget_amount
    return is_breached, cost_amount, budget_amount, currency_code


def disable_cloud_run_service(
    project_id: str,
    region: str,
    service_name: str,
    dry_run: bool = False,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Calls Google Cloud Run Admin API v1 / v2 to disable analysis and scale instances to 0.
    """
    action_summary: Dict[str, Any] = {
        "project_id": project_id,
        "region": region,
        "service_name": service_name,
        "dry_run": dry_run,
        "status": "pending",
        "action_taken": "scale_to_zero_and_disable_analysis",
    }

    if dry_run:
        logger.info(
            "[DRY-RUN] Would disable Cloud Run service '%s' in '%s/%s' (scaling max instances to 0).",
            service_name,
            project_id,
            region,
        )
        action_summary["status"] = "dry_run_success"
        return action_summary

    if not access_token:
        # Try retrieving GCP metadata access token if running inside GCP Cloud Function
        try:
            req = urllib.request.Request(
                "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
                headers={"Metadata-Flavor": "Google"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                token_data = json.loads(resp.read().decode())
                access_token = token_data.get("access_token")
        except Exception as err:
            logger.error("Unable to acquire metadata access token: %s", err)

    if not access_token:
        action_summary["status"] = "error"
        action_summary["error"] = "No Google access token available to authenticate Cloud Run Admin API"
        return action_summary

    url = f"https://run.googleapis.com/v2/projects/{project_id}/locations/{region}/services/{service_name}"
    update_mask = "template.scaling.maxInstanceCount,template.containers.env"
    patch_url = f"{url}?updateMask={update_mask}"

    payload = {
        "template": {
            "scaling": {"maxInstanceCount": 0},
            "containers": [
                {
                    "env": [
                        {"name": "LABELFIT_ENABLE_ANALYSIS", "value": "false"},
                        {"name": "LABELFIT_KILLSWITCH_ENGAGED", "value": "true"},
                    ]
                }
            ],
        }
    }

    req = urllib.request.Request(
        patch_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp_data = json.loads(resp.read().decode())
            action_summary["status"] = "success"
            action_summary["response"] = resp_data
            logger.info("Successfully patched Cloud Run service: scaled to 0, analysis disabled.")
    except urllib.error.HTTPError as http_err:
        err_msg = http_err.read().decode()
        logger.error("Cloud Run API returned HTTP %s: %s", http_err.code, err_msg)
        action_summary["status"] = "failed"
        action_summary["http_code"] = http_err.code
        action_summary["error"] = err_msg
    except Exception as exc:
        logger.error("Failed to execute Cloud Run update: %s", exc)
        action_summary["status"] = "error"
        action_summary["error"] = str(exc)

    return action_summary


def handle_budget_notification(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Entrypoint for GCP Cloud Function (Gen 2 / Gen 1) Pub/Sub event handler.
    """
    project_id = os.getenv("GCP_PROJECT_ID", "labelfit-india")
    service_name = os.getenv("CLOUD_RUN_SERVICE", "labelfit-backend")
    region = os.getenv("CLOUD_RUN_REGION", "asia-south1")
    dry_run = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")

    payload, err = parse_pubsub_message(event)
    if err:
        logger.error("Invalid Pub/Sub event: %s", err)
        return {"status": "error", "message": err}

    is_breached, cost, budget, currency = check_budget_breach(payload)
    logger.info(
        "Billing Notification: Cost=%s %s, Budget=%s %s, Breached=%s",
        cost,
        currency,
        budget,
        currency,
        is_breached,
    )

    if not is_breached:
        logger.info("Budget intact (%s / %s %s). No killswitch action required.", cost, budget, currency)
        return {
            "status": "ok",
            "action": "none",
            "cost": cost,
            "budget": budget,
            "currency": currency,
        }

    logger.critical(
        "CRITICAL: Budget breached! Current cost %s exceeds budget ceiling %s %s. Triggering killswitch!",
        cost,
        budget,
        currency,
    )

    result = disable_cloud_run_service(
        project_id=project_id,
        region=region,
        service_name=service_name,
        dry_run=dry_run,
    )
    result["cost"] = cost
    result["budget"] = budget
    result["currency"] = currency
    return result


if __name__ == "__main__":
    # Test runner for local simulation
    sample_breach_event = {
        "data": base64.b64encode(
            json.dumps({
                "budgetDisplayName": "LabelFit Monthly Safety Budget",
                "costAmount": 2150.0,
                "costIntervalStart": "2026-11-01T00:00:00Z",
                "budgetAmount": 2000.0,
                "currencyCode": "INR",
            }).encode("utf-8")
        ).decode("utf-8")
    }
    os.environ["DRY_RUN"] = "true"
    res = handle_budget_notification(sample_breach_event)
    print(json.dumps(res, indent=2))
