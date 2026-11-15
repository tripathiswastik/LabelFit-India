"""
Tests for LabelFit India CLI tools:
- scripts/transcribe_cli.py
- scripts/record_caregiver_session.py
- scripts/build_50sku_benchmark.py
"""

import os
import sys
import json
import tempfile
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
SCRIPTS_ROOT = REPO_ROOT / "scripts"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from labelfit.adjudication import AdjudicationEngine, DualTranscriptionRecord
import transcribe_cli
import record_caregiver_session
import build_50sku_benchmark


@pytest.fixture
def temp_transcription_csv():
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    records = [
        DualTranscriptionRecord(
            sku_id="SKU-BF-001",
            brand="Slurrp Farm",
            product_name="Supergrain Cereal",
            field="ingredients",
            swastik_transcription="Ragi, Jowar",
            swastik_date="2026-11-15",
            saumya_transcription="Ragi, Jowar",
            saumya_date="2026-11-15",
            adjudicated_ground_truth="Ragi, Jowar",
            adjudication_notes="Exact match",
        ),
        DualTranscriptionRecord(
            sku_id="SKU-BF-002",
            brand="Manna",
            product_name="Ragi Cereal",
            field="ageMarking",
            swastik_transcription="",
            swastik_date="",
            saumya_transcription="",
            saumya_date="",
            adjudicated_ground_truth="",
            adjudication_notes="",
        ),
    ]
    transcribe_cli.save_records(records, Path(path))
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_transcribe_cli_record_single(temp_transcription_csv):
    engine = AdjudicationEngine(temp_transcription_csv)
    records = engine.load()

    # Record for Swastik
    ok = transcribe_cli.record_single(
        records, "swastik", "SKU-BF-002", "ageMarking", "Stage 1: From 6 Months", "2026-11-15"
    )
    assert ok
    rec = [r for r in records if r.sku_id == "SKU-BF-002" and r.field == "ageMarking"][0]
    assert rec.swastik_transcription == "Stage 1: From 6 Months"
    assert rec.swastik_date == "2026-11-15"
    assert not rec.is_adjudicated

    # Record matching text for Saumya -> should auto-concur
    ok = transcribe_cli.record_single(
        records, "saumya", "SKU-BF-002", "ageMarking", "Stage 1: From 6 Months", "2026-11-15"
    )
    assert ok
    assert rec.is_adjudicated
    assert rec.adjudicated_ground_truth == "Stage 1: From 6 Months"


def test_transcribe_cli_invalid_reviewer(temp_transcription_csv):
    engine = AdjudicationEngine(temp_transcription_csv)
    records = engine.load()
    ok = transcribe_cli.record_single(
        records, "unknown_person", "SKU-BF-002", "ageMarking", "text", "2026-11-15"
    )
    assert not ok


def test_transcribe_cli_batch_import(temp_transcription_csv):
    engine = AdjudicationEngine(temp_transcription_csv)
    records = engine.load()

    fd, json_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    entries = [
        {
            "reviewer": "swastik",
            "sku_id": "SKU-BF-002",
            "field": "ageMarking",
            "text": "From 6 Months",
            "date": "2026-11-15",
            "notes": "Verified on back flap",
        }
    ]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f)

    try:
        for entry in entries:
            transcribe_cli.record_single(
                records,
                entry["reviewer"],
                entry["sku_id"],
                entry["field"],
                entry["text"],
                entry["date"],
                entry["notes"],
            )
        transcribe_cli.save_records(records, Path(temp_transcription_csv))
        reloaded = engine.load()
        target = [r for r in reloaded if r.sku_id == "SKU-BF-002" and r.field == "ageMarking"][0]
        assert target.swastik_transcription == "From 6 Months"
        assert "Verified on back flap" in target.adjudication_notes
    finally:
        if os.path.exists(json_path):
            os.remove(json_path)


def test_caregiver_session_append_trial():
    fd, csv_path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)

    try:
        row = {
            "session_id": "SESS-TEST-01",
            "caregiver_id": "CG-01",
            "sku_id": "SKU-BF-001",
            "task_type": "age_marking",
            "time_without_tool_sec": "15.4",
            "time_with_tool_sec": "4.2",
            "accuracy_check": "true",
            "understood_read_status": "true",
            "relied_on_physical_pack": "true",
            "misinterpreted_as_safety_score": "false",
            "feedback_notes": "Promptly found Stage 1 label",
        }
        record_caregiver_session.append_trial(row, Path(csv_path))

        evaluator = record_caregiver_session.UsabilityEvaluator(csv_path)
        res = evaluator.evaluate()
        assert res["total_trials"] == 1
        assert res["unique_caregivers"] == 1
        assert res["safety_misinterpretation_count"] == 0
        assert res["time_reduction_pct"] > 70.0
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_build_50sku_benchmark_strata():
    assert "Stratum 1" in build_50sku_benchmark.get_stratum_name("SKU-BF-005")
    assert "Stratum 2" in build_50sku_benchmark.get_stratum_name("SKU-BF-015")
    assert "Stratum 3" in build_50sku_benchmark.get_stratum_name("SKU-BF-025")
    assert "Stratum 4" in build_50sku_benchmark.get_stratum_name("SKU-BF-035")
    assert "Stratum 5" in build_50sku_benchmark.get_stratum_name("SKU-BF-045")
    assert build_50sku_benchmark.get_stratum_name("UNKNOWN-01") == "Other / Uncategorized"
