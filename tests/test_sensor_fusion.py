"""
Unit and Integration Tests for Research-Grade Adaptive Multi-Sensor Fusion Engine (Part 3)
Verifies adaptive weighting, health penalties, weather adaptations, sensor disagreement analysis,
missing sensor handling, and diagnostic explainability outputs.
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fusion.fusion import adaptive_sensor_fusion
from fusion.config import BASE_RELIABILITIES, WEATHER_MODIFIERS, HEALTH_PENALTIES
from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from simulator.profiles import AircraftType


class TestSensorFusionEngine(unittest.TestCase):

    def test_output_fields_completeness(self):
        """Verify fusion engine produces all required output metrics and explanation fields."""
        sensor_scores = {"Radar": 0.85, "Infrared": 0.70, "Thermal": 0.65, "Acoustic": 0.40, "EO_Camera": 0.75}
        env_data = {"weather": "Clear", "distance": 20.0, "jamming": 0.0, "sensor_health": {}}
        
        result = adaptive_sensor_fusion(sensor_scores, env_data)

        required_keys = [
            "fusion_score", "overall_confidence", "reliability_score", "uncertainty",
            "threat_confidence", "sensor_weights", "sensor_contributions", "sensor_rankings",
            "recommended_sensors", "sensor_health_summary", "disagreement_analysis",
            "environmental_adjustments", "explanation", "sensor_explanations", "fusion_metadata"
        ]
        for key in required_keys:
            self.assertIn(key, result, f"Missing key '{key}' in fusion engine output")

        self.assertIsInstance(result["fusion_score"], float)
        self.assertIsInstance(result["overall_confidence"], float)
        self.assertIsInstance(result["sensor_weights"], dict)
        self.assertIsInstance(result["explanation"], str)
        self.assertGreater(len(result["explanation"]), 0)

    def test_weather_adaptation_heavy_rain(self):
        """Verify Heavy Rain degrades Radar and EO_Camera weights relative to IR/Thermal."""
        scores = {"Radar": 0.80, "Infrared": 0.80, "Thermal": 0.80, "Acoustic": 0.80, "EO_Camera": 0.80}
        
        env_clear = {"weather": "Clear Day", "distance": 15.0}
        env_rain = {"weather": "Heavy Rain", "distance": 15.0}

        fusion_clear = adaptive_sensor_fusion(scores, env_clear)
        fusion_rain = adaptive_sensor_fusion(scores, env_rain)

        # Under Heavy Rain, Radar & Camera weights decrease compared to Clear Day
        self.assertLess(fusion_rain["sensor_weights"]["Radar"], fusion_clear["sensor_weights"]["Radar"])
        self.assertLess(fusion_rain["sensor_weights"]["EO_Camera"], fusion_clear["sensor_weights"]["EO_Camera"])
        
        # Infrared & Thermal weights increase in relative importance
        self.assertGreater(fusion_rain["sensor_weights"]["Infrared"], fusion_clear["sensor_weights"]["Infrared"])

    def test_electronic_jamming_adaptation(self):
        """Verify Electronic Jamming significantly penalizes Radar weight."""
        scores = {"Radar": 0.90, "Infrared": 0.90, "Thermal": 0.90, "Acoustic": 0.90, "EO_Camera": 0.90}
        env_jamming = {"weather": "Electronic Jamming", "distance": 15.0, "jamming": 0.8}

        fusion = adaptive_sensor_fusion(scores, env_jamming)
        
        self.assertLess(fusion["sensor_weights"]["Radar"], 0.15)
        self.assertIn("Infrared", fusion["recommended_sensors"])

    def test_sensor_offline_and_failure_handling(self):
        """Verify Offline or Jammed sensors are zero-weighted or heavily penalized without crashing."""
        scores = {"Radar": 0.0, "Infrared": 0.85, "Thermal": 0.80, "Acoustic": 0.40, "EO_Camera": 0.70}
        env_data = {
            "weather": "Clear",
            "distance": 20.0,
            "sensor_health": {"Radar": "Offline", "EO_Camera": "Jammed"}
        }

        fusion = adaptive_sensor_fusion(scores, env_data)
        
        self.assertEqual(fusion["sensor_weights"]["Radar"], 0.0)
        self.assertLess(fusion["sensor_weights"]["EO_Camera"], 0.10)
        self.assertGreater(fusion["fusion_score"], 0.50)  # IR and Thermal drive the score

    def test_disagreement_analysis_and_uncertainty(self):
        """Verify conflicting sensor observations trigger disagreement warning and elevate uncertainty."""
        # Conflicting readings: Radar & Thermal high (0.95), Camera & Acoustic low (0.05)
        scores = {"Radar": 0.95, "Infrared": 0.90, "Thermal": 0.95, "Acoustic": 0.05, "EO_Camera": 0.05}
        env_data = {"weather": "Clear", "distance": 15.0}

        fusion = adaptive_sensor_fusion(scores, env_data)

        self.assertTrue(fusion["disagreement_analysis"]["disagreements_found"])
        self.assertGreater(fusion["uncertainty"], 0.20)
        self.assertIn("conflict", fusion["explanation"].lower())

    def test_aircraft_profile_fusion_integration(self):
        """Verify fusion engine works across all aircraft profile scenarios generated by Part 1 & 2."""
        for aircraft_type in AircraftType:
            env = generate_environment(aircraft_type=aircraft_type, seed=123)
            scores = calculate_sensor_scores(env, seed=123)

            fusion_result = adaptive_sensor_fusion(scores, env)
            
            self.assertGreaterEqual(fusion_result["fusion_score"], 0.0)
            self.assertLessEqual(fusion_result["fusion_score"], 1.0)
            self.assertIn(fusion_result["sensor_rankings"][0], ["Radar", "Infrared", "Thermal", "Acoustic", "EO_Camera"])

    def test_missing_sensor_handling(self):
        """Verify fusion engine handles missing keys in sensor_scores gracefully."""
        partial_scores = {"Radar": 0.75, "Infrared": 0.80}  # Thermal, Acoustic, EO_Camera missing
        env_data = {"weather": "Clear", "distance": 10.0}

        fusion = adaptive_sensor_fusion(partial_scores, env_data)

        self.assertIsNotNone(fusion["fusion_score"])
        self.assertIn("Radar", fusion["sensor_weights"])


if __name__ == "__main__":
    unittest.main()
