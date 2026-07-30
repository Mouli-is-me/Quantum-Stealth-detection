"""
Unit and Integration Tests for Explainable AI & Intelligent Threat Classification (Part 4)
Verifies target classification across 7 profiles, feature importances, threat level assessment,
uncertainty analysis, systematic explanations, recommendations, and backward compatibility.
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.predict import predict, predict_explainable
from ai.xai_engine import XAIEngine
from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from fusion.fusion import adaptive_sensor_fusion
from simulator.profiles import AircraftType


class TestExplainableAI(unittest.TestCase):

    def test_legacy_predict_tuple_return(self):
        """Verify predict(sensor_data) returns a 2-element tuple (prediction: int, confidence: float)."""
        env = generate_environment()
        scores = calculate_sensor_scores(env)
        data = {**env, **scores}

        result = predict(data)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        prediction, confidence = result

        self.assertIn(prediction, [0, 1])
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_predict_explainable_fields(self):
        """Verify predict_explainable produces all required XAI fields and metrics."""
        env = generate_environment(aircraft_type=AircraftType.STEALTH_FIGHTER)
        scores = calculate_sensor_scores(env)
        data = {**env, **scores}

        xai_res = predict_explainable(data)

        required_keys = [
            "prediction", "confidence", "predicted_class", "prediction_probability",
            "threat_level", "feature_importance", "top_contributing_sensors",
            "reasoning", "uncertainty", "recommendation", "ai_metadata"
        ]
        for key in required_keys:
            self.assertIn(key, xai_res, f"Missing key '{key}' in XAI result")

        self.assertEqual(xai_res["predicted_class"], "Stealth Fighter")
        self.assertIn(xai_res["threat_level"], ["Low", "Medium", "High", "Critical"])
        self.assertIsInstance(xai_res["feature_importance"], dict)
        self.assertIsInstance(xai_res["reasoning"], str)
        self.assertGreater(len(xai_res["reasoning"]), 0)

    def test_all_7_target_classifications(self):
        """Test target classification across all 7 target profile categories."""
        target_map = {
            AircraftType.COMMERCIAL: "Commercial Aircraft",
            AircraftType.STEALTH_FIGHTER: "Stealth Fighter",
            AircraftType.RECON_DRONE: "Recon Drone",
            AircraftType.CRUISE_MISSILE: "Cruise Missile",
            AircraftType.HELICOPTER: "Helicopter",
            AircraftType.BIRD: "Bird",
            AircraftType.UNKNOWN: "Unknown Object"
        }

        for atype, expected_class in target_map.items():
            env = generate_environment(aircraft_type=atype, seed=42)
            scores = calculate_sensor_scores(env, seed=42)
            data = {**env, **scores}

            xai_res = predict_explainable(data)
            self.assertEqual(xai_res["predicted_class"], expected_class)

    def test_threat_level_assessment(self):
        """Verify Threat Level assessment appropriately flags Cruise Missile / Stealth Fighter vs Commercial / Bird."""
        env_missile = generate_environment(aircraft_type=AircraftType.CRUISE_MISSILE, distance=15.0)
        data_missile = {**env_missile, **calculate_sensor_scores(env_missile)}
        xai_missile = predict_explainable(data_missile)
        self.assertIn(xai_missile["threat_level"], ["High", "Critical"])

        env_bird = generate_environment(aircraft_type=AircraftType.BIRD)
        data_bird = {**env_bird, **calculate_sensor_scores(env_bird)}
        xai_bird = predict_explainable(data_bird)
        self.assertEqual(xai_bird["threat_level"], "Low")

    def test_feature_importance_sum_to_one(self):
        """Verify feature importance values sum to 1.0 (100%)."""
        env = generate_environment()
        scores = calculate_sensor_scores(env)
        data = {**env, **scores}

        xai_res = predict_explainable(data)
        importances = xai_res["feature_importance"]
        
        total_imp = sum(importances.values())
        self.assertAlmostEqual(total_imp, 1.0, places=2)

    def test_uncertainty_analysis_with_fusion(self):
        """Verify uncertainty analysis integrates fusion results and stays bounded [0.0, 1.0]."""
        env = generate_environment(weather="Fog")
        scores = calculate_sensor_scores(env)
        data = {**env, **scores}

        fusion_res = adaptive_sensor_fusion(scores, env)
        xai_res = predict_explainable(data, fusion_result=fusion_res)

        self.assertGreaterEqual(xai_res["uncertainty"], 0.0)
        self.assertLessEqual(xai_res["uncertainty"], 1.0)

    def test_recommendation_and_reasoning_content(self):
        """Verify generated reasoning and tactical recommendation text are non-empty and descriptive."""
        env = generate_environment(aircraft_type=AircraftType.STEALTH_FIGHTER, weather="Night")
        data = {**env, **calculate_sensor_scores(env)}

        xai_res = predict_explainable(data)

        self.assertIn("Stealth Fighter", xai_res["reasoning"])
        self.assertIn("THREAT", xai_res["recommendation"])


if __name__ == "__main__":
    unittest.main()
