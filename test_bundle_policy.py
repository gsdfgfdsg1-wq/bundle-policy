import unittest
from bundle_policy import evaluate


class BundlePolicyTests(unittest.TestCase):
    def test_passes_within_budget(self):
        report = evaluate({"assets": [{"name": "app.js", "bytes": 50, "route": "/"}]}, {"budgets": {"total": 100, "type:script": 80}})
        self.assertTrue(report["ok"])
        self.assertEqual(report["totals"]["route:/"], 50)

    def test_reports_route_overage(self):
        report = evaluate({"assets": [{"name": "checkout.js", "bytes": 120, "route": "/checkout"}]}, {"budgets": {"route:/checkout": 100}})
        self.assertFalse(report["ok"])
        self.assertEqual(report["violations"][0]["over"], 20)

    def test_tracks_third_party_hosts(self):
        report = evaluate({"assets": [{"name": "https://cdn.example/a.js", "bytes": 33}]}, {"budgets": {"third-party:cdn.example": 30}})
        self.assertEqual(report["totals"]["third-party:cdn.example"], 33)
        self.assertFalse(report["ok"])


if __name__ == "__main__":
    unittest.main()
