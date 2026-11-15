import csv
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from labelfit.scan_runs import _read_worksheet, _write_worksheet, apply_run, load_run  # noqa: E402

COLUMNS = ["image_id", "sku_id", "brand", "market_city", "package_language_script", "photo_condition", "field",
           "ground_truth", "model_output", "read_status", "evidence_located", "unsupported_text",
           "error_category", "review_seconds", "reviewer_notes"]
REPO_WORKSHEET = os.path.join(os.path.dirname(__file__), "..", "docs", "benchmark-50sku-results.csv")


def pending(image, field, gt="Truth text", notes="Verified."):
    return {"image_id": image, "sku_id": image.replace("IMG-", ""), "brand": "B", "market_city": "Delhi",
            "package_language_script": "English-Latin", "photo_condition": "pouch_panel", "field": field,
            "ground_truth": gt, "model_output": "", "read_status": "pending_model_scan",
            "evidence_located": "no", "unsupported_text": "no", "error_category": "pending_model_scan",
            "review_seconds": "", "reviewer_notes": notes}


def record(image, ok=True, text="Model text"):
    field = {"value": text, "evidence": "snip", "readStatus": "clear"}
    base = {"run_id": "r1", "image_id": image, "sku_id": image.replace("IMG-", ""), "model_responded": "gemini-x"}
    if ok:
        return {**base, "error": None, "normalized": {n: field for n in
                ("productName", "ageMarking", "ingredients", "allergenDeclaration", "nutritionPanel", "preparationAndStorage")}}
    return {**base, "error": {"stage": "model", "status": 502, "message": "boom"}}


class ApplyRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.run_dir = os.path.join(self.dir, "run")
        os.makedirs(self.run_dir)
        self.sheet = os.path.join(self.dir, "sheet.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def write_sheet(self, rows, bom=True, newline="\n"):
        with open(self.sheet, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator=newline)
            writer.writeheader()
            writer.writerows(rows)

    def write_run(self, records):
        with open(os.path.join(self.run_dir, "run.json"), "w", encoding="utf-8") as f:
            json.dump({"run_id": "r1", "model_requested": "gemini-x", "prompt_fingerprint": "abc123"}, f)
        for r in records:
            with open(os.path.join(self.run_dir, f"{r['image_id']}.json"), "w", encoding="utf-8") as f:
                json.dump(r, f)

    def read_rows(self):
        with open(self.sheet, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def test_fills_only_pending_rows_and_never_touches_ground_truth(self):
        done = pending("IMG-SKU-9", "ingredients")
        done.update(model_output="Existing output", read_status="clear", evidence_located="yes", error_category="none")
        self.write_sheet([pending("IMG-SKU-1", "ingredients"), pending("IMG-SKU-1", "productName"), done])
        self.write_run([record("IMG-SKU-1"), record("IMG-SKU-9")])
        summary = apply_run(self.sheet, self.run_dir)
        rows = self.read_rows()
        self.assertEqual(summary["filled_rows"], 2)
        self.assertEqual(summary["skipped_not_pending"], 1)
        for r in rows[:2]:
            self.assertEqual(r["model_output"], "Model text")
            self.assertEqual(r["read_status"], "clear")
            self.assertEqual(r["ground_truth"], "Truth text")
        self.assertEqual(rows[2]["model_output"], "Existing output")
        self.assertEqual(rows[2]["error_category"], "none")

    def test_reviewer_columns_are_reset_not_faked(self):
        self.write_sheet([pending("IMG-SKU-1", "ingredients")])
        self.write_run([record("IMG-SKU-1")])
        apply_run(self.sheet, self.run_dir)
        row = self.read_rows()[0]
        self.assertEqual((row["evidence_located"], row["unsupported_text"], row["error_category"]), ("", "", "unreviewed"))
        self.assertIn("Verified.", row["reviewer_notes"])
        self.assertIn("auto-filled from run r1", row["reviewer_notes"])
        self.assertIn("gemini-x", row["reviewer_notes"])

    def test_failed_scans_are_skipped_not_scored_as_misses(self):
        self.write_sheet([pending("IMG-SKU-1", "ingredients"), pending("IMG-SKU-2", "ingredients")])
        self.write_run([record("IMG-SKU-1", ok=False), record("IMG-SKU-2")])
        summary = apply_run(self.sheet, self.run_dir)
        rows = self.read_rows()
        self.assertEqual(summary["skipped_failed_scan"], ["IMG-SKU-1"])
        self.assertEqual(rows[0]["read_status"], "pending_model_scan")
        self.assertEqual(rows[0]["model_output"], "")
        self.assertEqual(rows[1]["read_status"], "clear")

    def test_images_without_a_record_stay_pending(self):
        self.write_sheet([pending("IMG-SKU-1", "ingredients"), pending("IMG-SKU-7", "ingredients")])
        self.write_run([record("IMG-SKU-1")])
        summary = apply_run(self.sheet, self.run_dir)
        self.assertEqual(summary["skipped_no_record"], ["IMG-SKU-7"])
        self.assertEqual(self.read_rows()[1]["read_status"], "pending_model_scan")

    def test_never_overwrites_existing_model_output(self):
        row = pending("IMG-SKU-1", "ingredients")
        row["model_output"] = "Typed by hand"
        self.write_sheet([row])
        self.write_run([record("IMG-SKU-1")])
        summary = apply_run(self.sheet, self.run_dir)
        self.assertEqual(summary["skipped_already_has_output"], 1)
        self.assertEqual(self.read_rows()[0]["model_output"], "Typed by hand")

    def test_dry_run_writes_nothing(self):
        self.write_sheet([pending("IMG-SKU-1", "ingredients")])
        self.write_run([record("IMG-SKU-1")])
        before = open(self.sheet, "rb").read()
        summary = apply_run(self.sheet, self.run_dir, dry_run=True)
        self.assertEqual(summary["filled_rows"], 1)
        self.assertEqual(open(self.sheet, "rb").read(), before)

    def test_file_format_is_preserved(self):
        self.write_sheet([pending("IMG-SKU-1", "ingredients")], bom=True, newline="\n")
        self.write_run([record("IMG-SKU-1")])
        apply_run(self.sheet, self.run_dir)
        raw = open(self.sheet, "rb").read()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r\n", raw)
        self.write_sheet([pending("IMG-SKU-1", "ingredients")], bom=False, newline="\r\n")
        apply_run(self.sheet, self.run_dir)
        raw = open(self.sheet, "rb").read()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertIn(b"\r\n", raw)

    def test_multiline_and_quoted_fields_survive(self):
        tricky = pending("IMG-SKU-1", "ingredients", gt='Line one,\nline "two"')
        self.write_sheet([tricky, pending("IMG-SKU-2", "ingredients")])
        self.write_run([record("IMG-SKU-2")])
        apply_run(self.sheet, self.run_dir)
        self.assertEqual(self.read_rows()[0]["ground_truth"], 'Line one,\nline "two"')

    def test_not_a_run_folder(self):
        self.write_sheet([pending("IMG-SKU-1", "ingredients")])
        with self.assertRaises(FileNotFoundError):
            apply_run(self.sheet, self.dir)

    def test_missing_columns_rejected(self):
        with open(self.sheet, "w", encoding="utf-8", newline="") as f:
            f.write("image_id,field\nIMG-1,ingredients\n")
        self.write_run([record("IMG-1")])
        with self.assertRaises(ValueError):
            apply_run(self.sheet, self.run_dir)

    def test_real_worksheet_round_trips_byte_for_byte(self):
        fieldnames, rows, bom, newline = _read_worksheet(REPO_WORKSHEET)
        out = os.path.join(self.dir, "copy.csv")
        _write_worksheet(out, fieldnames, rows, bom, newline)
        self.assertEqual(open(out, "rb").read(), open(REPO_WORKSHEET, "rb").read())

    def test_load_run(self):
        self.write_run([record("IMG-SKU-1")])
        meta, records = load_run(self.run_dir)
        self.assertEqual(meta["run_id"], "r1")
        self.assertIn("IMG-SKU-1", records)


if __name__ == "__main__":
    unittest.main()
