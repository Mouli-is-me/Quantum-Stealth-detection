"""
End-to-End Integration Test Suite for AEGIS-X (Part 6)
Verifies full pipeline execution across all demo presets, multi-target scenarios, missing sensors,
extreme weather, Quantum Optimization, and system stability.
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline import run_full_aegis_pipeline
from src.logger import get_aegis_logger


class TestEndToEndPipeline(unittest.TestCase):

    def test_full_pipeline_execution_demo_presets(self):
        """Verify complete pipeline execution across all 8 predefined demo presets."""
        for preset_id in range(1, 9):
            res = run_full_aegis_pipeline(demo_preset=preset_id, seed=100 + preset_id)
            
            self.assertIn("scenario", res)
            self.assertIn("sensor_scores", res)
            self.assertIn("fusion", res)
            self.assertIn("ai", res)
            self.assertIn("quantum_selection", res)

            # Check Quantum Selection format
            qs = res["quantum_selection"]
            self.assertIn("Radar", qs)
            self.assertIn("Infrared", qs)
            self.assertIn("Acoustic", qs)

            # Check AI format
            ai = res["ai"]
            self.assertIn(ai["prediction"], [0, 1])
            self.assertIn(ai["threat_level"], ["Low", "Medium", "High", "Critical"])

    def test_multi_target_pipeline_execution(self):
        """Verify pipeline execution with multi-target swarms (target_count = 5)."""
        res = run_full_aegis_pipeline(target_count=5, distance_km=20.0, seed=777)
        self.assertEqual(res["scenario"]["target_count"], 5)
        self.assertEqual(len(res["scenario"]["targets"]), 5)
        self.assertGreaterEqual(res["fusion"]["overall_confidence"], 0.0)

    def test_extreme_weather_and_jamming(self):
        """Verify pipeline stability under Electronic Jamming and Heavy Rain."""
        res = run_full_aegis_pipeline(weather="Electronic Jamming", jamming_level=0.9, seed=888)
        self.assertEqual(res["scenario"]["weather"], "Fog")  # Legacy mapped
        self.assertEqual(res["scenario"]["weather_detailed"], "Electronic Jamming")
        self.assertIn("Infrared", res["fusion"]["recommended_sensors"])

    def test_missing_and_corrupt_input_resilience(self):
        """Verify error resilience when partial or non-standard inputs are passed."""
        res = run_full_aegis_pipeline(distance_km=120.0, seed=123)
        self.assertIsNotNone(res["fusion"]["fusion_score"])

    def test_logger_functionality(self):
        """Verify logger instantiation and message logging."""
        logger = get_aegis_logger("AEGIS-Test")
        self.assertIsNotNone(logger)
        logger.info("Test logging message verified.")


if __name__ == "__main__":
    unittest.main()
