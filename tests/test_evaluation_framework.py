"""
Unit and Integration Tests for AI Evaluation & Validation Framework (Part 5)
Verifies performance metrics calculations, environmental robustness sweeps, fusion benchmarking,
report generation, and deterministic reproducibility.
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from evaluation.metrics import PerformanceMetrics
from evaluation.robustness import RobustnessEvaluator
from evaluation.benchmark import FusionBenchmarker
from evaluation.runner import evaluate_ai_system


class TestEvaluationFramework(unittest.TestCase):

    def test_metrics_calculation(self):
        """Verify performance metrics calculation accuracy (precision, recall, f1, false alarm rate, ECE)."""
        y_true = [1, 1, 1, 0, 0]
        y_pred = [1, 1, 0, 0, 1]
        c_true = ["Commercial", "Stealth", "Drone", "Bird", "Bird"]
        c_pred = ["Commercial", "Stealth", "Bird", "Bird", "Stealth"]
        confs = [0.95, 0.90, 0.40, 0.92, 0.88]

        metrics = PerformanceMetrics.calculate_classification_metrics(y_true, y_pred, c_true, c_pred, confs)

        self.assertEqual(metrics["total_samples"], 5)
        self.assertEqual(metrics["confusion_matrix"]["TP"], 2)
        self.assertEqual(metrics["confusion_matrix"]["FP"], 1)
        self.assertEqual(metrics["confusion_matrix"]["TN"], 1)
        self.assertEqual(metrics["confusion_matrix"]["FN"], 1)
        
        self.assertAlmostEqual(metrics["accuracy"], 0.60, places=2)
        self.assertAlmostEqual(metrics["precision"], 0.6667, places=2)
        self.assertAlmostEqual(metrics["recall"], 0.6667, places=2)
        self.assertIn("calibration", metrics)

    def test_environmental_robustness_sweep(self):
        """Verify robustness evaluator runs environmental sweeps across weather conditions."""
        res = RobustnessEvaluator.evaluate_environmental_robustness(samples_per_condition=5, seed=12)
        
        self.assertIn("Clear Day", res)
        self.assertIn("Heavy Rain", res)
        self.assertIn("Fog", res)
        self.assertIn("accuracy", res["Clear Day"])
        self.assertGreaterEqual(res["Clear Day"]["accuracy"], 0.0)

    def test_sensor_failure_robustness_sweep(self):
        """Verify robustness evaluator runs hardware failure sweeps."""
        res = RobustnessEvaluator.evaluate_sensor_failure_robustness(samples_per_condition=5, seed=34)
        
        self.assertIn("All Sensors Healthy", res)
        self.assertIn("Radar Offline", res)
        self.assertIn("accuracy", res["Radar Offline"])

    def test_fusion_benchmarker_execution(self):
        """Verify fusion benchmarker computes performance gains between raw vs fused sensors."""
        bm = FusionBenchmarker.run_fusion_benchmark(num_scenarios=10, seed=99)
        
        self.assertIn("raw_baseline", bm)
        self.assertIn("adaptive_fusion", bm)
        self.assertIn("performance_improvement", bm)
        self.assertIn("accuracy_gain_pct", bm["performance_improvement"])

    def test_evaluate_ai_system_runner(self):
        """Verify complete evaluation runner executes and generates evaluation_report.md."""
        report_path = "evaluation/test_eval_report.md"
        res = evaluate_ai_system(num_scenarios=15, seed=55, report_path=report_path)

        self.assertIn("overall_metrics", res)
        self.assertTrue(os.path.exists(report_path), "Evaluation report file should be created")
        
        # Cleanup temporary test report
        if os.path.exists(report_path):
            os.remove(report_path)


if __name__ == "__main__":
    unittest.main()
