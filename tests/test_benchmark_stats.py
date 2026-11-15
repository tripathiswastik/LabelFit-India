import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from labelfit.benchmark_stats import (  # noqa: E402
    classify_row, cluster_bootstrap_rate, evaluate_csv, extract_numbers,
    format_markdown, numbers_match, summarize, wilson_interval,
)

COLUMNS = ["image_id", "sku_id", "brand", "market_city", "package_language_script", "photo_condition", "field",
           "ground_truth", "model_output", "read_status", "evidence_located", "unsupported_text",
           "error_category", "review_seconds", "reviewer_notes"]


def make_row(sku="SKU-1", field="ingredients", gt="Rice flour, sugar", out=None, status="clear",
             brand="BrandA", script="English-Latin", condition="pouch_panel",
             evidence="yes", unsupported="no", category="none", seconds=""):
    return {"image_id": f"IMG-{sku}", "sku_id": sku, "brand": brand, "market_city": "Delhi",
            "package_language_script": script, "photo_condition": condition, "field": field,
            "ground_truth": gt, "model_output": gt if out is None else out, "read_status": status,
            "evidence_located": evidence, "unsupported_text": unsupported, "error_category": category,
            "review_seconds": seconds, "reviewer_notes": ""}


class WilsonTests(unittest.TestCase):
    def test_known_values(self):
        low, high = wilson_interval(0, 10)
        self.assertAlmostEqual(low, 0.0, places=4)
        self.assertAlmostEqual(high, 0.2775, places=3)
        low, high = wilson_interval(10, 10)
        self.assertAlmostEqual(low, 0.7225, places=3)
        self.assertAlmostEqual(high, 1.0, places=4)
        low, high = wilson_interval(5, 10)
        self.assertAlmostEqual(low, 0.2366, places=3)
        self.assertAlmostEqual(high, 0.7634, places=3)

    def test_no_observations_gives_no_interval(self):
        self.assertIsNone(wilson_interval(0, 0))

    def test_small_sample_is_wide(self):
        low, high = wilson_interval(1, 1)
        self.assertLess(low, 0.25)


class NumberTests(unittest.TestCase):
    def test_changed_number_is_caught(self):
        self.assertFalse(numbers_match("Iron 12.5 mg", "Iron 1.25 mg"))
        self.assertFalse(numbers_match("Suitable 6 months+", "Suitable 8 months+"))

    def test_same_numbers_match_regardless_of_spacing_or_order(self):
        self.assertTrue(numbers_match("Iron 12.5 mg, Zinc 3 mg", "Zinc 3mg Iron 12.5mg"))

    def test_devanagari_digits_equal_ascii(self):
        self.assertEqual(extract_numbers("१२.५ mg"), ["12.5"])
        self.assertTrue(numbers_match("लोह १२.५ mg", "iron 12.5 mg"))

    def test_no_numbers_on_either_side_matches(self):
        self.assertTrue(numbers_match("Rice flour", "Rice flour"))


class ClassifyTests(unittest.TestCase):
    def test_readable_but_wrong(self):
        c = classify_row(make_row(out="Rice flour, suger"))
        self.assertTrue(c["clear"] and c["wrong_clear"] and not c["exact"])

    def test_uncertain_wrong_is_not_a_false_readable(self):
        c = classify_row(make_row(out="Rice flour, suger", status="uncertain"))
        self.assertFalse(c["wrong_clear"])

    def test_readable_with_changed_number(self):
        c = classify_row(make_row(field="nutritionPanel", gt="Iron 12.5 mg", out="Iron 1.25 mg"))
        self.assertTrue(c["clear_number_mismatch"])

    def test_hallucination_and_missed_field(self):
        h = classify_row(make_row(gt="", out="Contains milk", status="clear"))
        self.assertTrue(h["hallucinated_absent"])
        m = classify_row(make_row(gt="Contains milk", out="", status="not_visible"))
        self.assertTrue(m["not_visible_miss"])
        ok = classify_row(make_row(gt="", out="", status="not_visible"))
        self.assertTrue(ok["exact"] and not ok["hallucinated_absent"] and not ok["not_visible_miss"])

    def test_unreviewed_rows_are_not_counted_as_reviewed(self):
        self.assertFalse(classify_row(make_row(evidence="", unsupported="", category="unreviewed"))["reviewed"])
        self.assertFalse(classify_row(make_row(category="pending_model_scan"))["reviewed"])
        self.assertTrue(classify_row(make_row())["reviewed"])


class ClusterBootstrapTests(unittest.TestCase):
    def test_too_few_skus_gives_none(self):
        self.assertIsNone(cluster_bootstrap_rate({f"s{i}": (0, 3) for i in range(4)}))

    def test_repeatable_with_same_seed(self):
        groups = {f"s{i}": (i % 2, 3) for i in range(12)}
        self.assertEqual(cluster_bootstrap_rate(groups, 500, seed=7), cluster_bootstrap_rate(groups, 500, seed=7))

    def test_interval_brackets_point_estimate(self):
        groups = {f"s{i}": (1 if i % 4 == 0 else 0, 4) for i in range(20)}
        point = sum(s for s, _ in groups.values()) / sum(t for _, t in groups.values())
        low, high = cluster_bootstrap_rate(groups, 1000, seed=3)
        self.assertLessEqual(low, point)
        self.assertGreaterEqual(high, point)

    def test_clustering_is_wider_than_independence_when_errors_cluster(self):
        # All errors sit in two SKUs: row-level Wilson would look tighter than the truth.
        groups = {f"s{i}": ((6, 6) if i < 2 else (0, 6)) for i in range(10)}
        low, high = cluster_bootstrap_rate(groups, 2000, seed=1)
        wl, wh = wilson_interval(12, 60)
        self.assertGreater(high - low, wh - wl)


class SummarizeTests(unittest.TestCase):
    def rows(self, n_skus=6):
        rows = []
        for i in range(n_skus):
            sku = f"SKU-{i}"
            rows.append(make_row(sku=sku, field="ingredients", brand=f"B{i}"))
            rows.append(make_row(sku=sku, field="nutritionPanel", gt="Iron 12.5 mg", out="Iron 12.5 mg", brand=f"B{i}"))
        return rows

    def test_counts_and_perfect_scores(self):
        s = summarize(self.rows())
        self.assertEqual((s["scored_rows"], s["unique_skus"]), (12, 6))
        self.assertEqual(s["readable_overall"]["wrong"], 0)
        self.assertEqual(s["by_field"]["ingredients"]["exact"], 6)
        self.assertIsNotNone(s["readable_overall"]["sku_cluster_bootstrap_ci95"])

    def test_wrong_readable_is_counted_and_in_report(self):
        rows = self.rows()
        rows[0]["model_output"] = "Rice flour, suger"
        rows[1]["model_output"] = "Iron 1.25 mg"
        s = summarize(rows)
        self.assertEqual(s["readable_overall"]["wrong"], 2)
        self.assertEqual(s["readable_overall"]["number_mismatches"], 1)
        self.assertIn("did not exactly match", format_markdown(s))

    def test_small_strata_are_suppressed(self):
        s = summarize(self.rows(), min_rows=20)
        self.assertTrue(all(v["suppressed"] for v in s["by_script"].values()))
        self.assertIn("too few to report", format_markdown(s))
        s = summarize(self.rows(), min_rows=10, min_skus=5)
        self.assertFalse(s["by_script"]["English-Latin"]["suppressed"])

    def test_single_sku_warns_and_gives_no_cluster_interval(self):
        s = summarize(self.rows(n_skus=1))
        self.assertIsNone(s["readable_overall"]["sku_cluster_bootstrap_ci95"])
        self.assertTrue(any("SKU(s) scored" in w for w in s["warnings"]))

    def test_unreviewed_rows_suppress_support_metrics(self):
        rows = self.rows()
        rows[0].update(evidence_located="", unsupported_text="", error_category="unreviewed")
        s = summarize(rows)
        self.assertEqual(s["review"]["reviewer_pending"], 1)
        self.assertNotIn("snippet_located", s["review"])
        self.assertTrue(any("reviewer columns" in w for w in s["warnings"]))

    def test_fully_reviewed_rows_report_support_metrics(self):
        s = summarize(self.rows())
        self.assertEqual(s["review"]["snippet_located"], 12)

    def test_concentrated_brand_and_single_script_warn(self):
        rows = [make_row(sku=f"S{i}", brand="OnlyBrand") for i in range(6)]
        s = summarize(rows)
        text = " ".join(s["warnings"])
        self.assertIn("concentrated", text)
        self.assertIn("one script", text.lower())

    def test_empty_input(self):
        s = summarize([], pending_excluded=3)
        self.assertEqual(s["scored_rows"], 0)
        self.assertIn("No completed", format_markdown(s))

    def test_review_time_only_when_measured(self):
        rows = self.rows()
        rows[0]["review_seconds"] = "30"
        rows[1]["review_seconds"] = "50"
        s = summarize(rows)
        self.assertEqual(s["review"]["review_seconds_measured"], 2)
        self.assertEqual(s["review"]["review_seconds_median"], 40)


class EvaluateCsvTests(unittest.TestCase):
    def test_pending_rows_are_excluded(self):
        rows = [make_row(sku="SKU-A"), make_row(sku="SKU-B", out="", status="pending_model_scan", category="pending_model_scan")]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "w.csv")
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            s = evaluate_csv(path)
        self.assertEqual(s["scored_rows"], 1)
        self.assertEqual(s["pending_rows_excluded"], 1)


if __name__ == "__main__":
    unittest.main()
