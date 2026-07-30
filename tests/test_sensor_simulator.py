"""
Unit and Integration Tests for Research-Grade Physics Synthetic Sensor Simulator
Verifies profiles, weather effects, sensor health, noise reproducibility, explainability,
and strict backward compatibility with existing AI, Quantum, and Dashboard modules.
"""

import sys
import os
import unittest
import numpy as np

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from simulator.profiles import AircraftType, PROFILES
from simulator.environment import Weather, SensorHealth
from ai.predict import predict
from quantum.optimizer import optimize_sensors


class TestSensorSimulator(unittest.TestCase):

    def test_legacy_interface_keys(self):
        """Verify generate_environment and calculate_sensor_scores produce required legacy keys and types."""
        env = generate_environment()
        
        # Check required legacy environment keys
        for key in ["distance", "weather", "stealth", "engine_heat", "noise"]:
            self.assertIn(key, env, f"Missing legacy key '{key}' in environment output")

        self.assertIsInstance(env["distance"], (int, float))
        self.assertIsInstance(env["weather"], str)
        self.assertIsInstance(env["stealth"], float)
        self.assertIsInstance(env["engine_heat"], float)
        self.assertIsInstance(env["noise"], float)

        scores = calculate_sensor_scores(env)

        # Check required legacy sensor keys
        for key in ["Radar", "Infrared", "Acoustic"]:
            self.assertIn(key, scores, f"Missing legacy sensor key '{key}' in scores output")
            self.assertIsInstance(scores[key], float, f"Score for '{key}' must be a float")
            self.assertGreaterEqual(scores[key], 0.0)
            self.assertLessEqual(scores[key], 1.0)

        # Check new sensor modalities and explainability
        self.assertIn("Thermal", scores)
        self.assertIn("EO_Camera", scores)
        self.assertIn("explanations", scores)
        self.assertIsInstance(scores["explanations"], dict)

    def test_all_aircraft_profiles(self):
        """Test simulation generation for all 7 aircraft profiles."""
        for aircraft_enum in AircraftType:
            env = generate_environment(aircraft_type=aircraft_enum, seed=123)
            scores = calculate_sensor_scores(env, seed=123)
            
            self.assertEqual(env["aircraft_type"], aircraft_enum.value)
            self.assertIn("Radar", scores)
            self.assertIn("Infrared", scores)
            self.assertIn("Acoustic", scores)

    def test_stealth_fighter_vs_commercial(self):
        """Verify Stealth Fighter has lower Radar score than Commercial Aircraft under identical conditions."""
        env_comm = generate_environment(aircraft_type=AircraftType.COMMERCIAL, distance=30.0, weather="Clear", jamming_level=0.0, seed=42)
        env_stealth = generate_environment(aircraft_type=AircraftType.STEALTH_FIGHTER, distance=30.0, weather="Clear", jamming_level=0.0, seed=42)

        scores_comm = calculate_sensor_scores(env_comm, seed=42)
        scores_stealth = calculate_sensor_scores(env_stealth, seed=42)

        self.assertGreater(
            scores_comm["Radar"],
            scores_stealth["Radar"],
            "Commercial aircraft should have higher radar visibility than stealth fighter"
        )

    def test_weather_effects(self):
        """Verify weather conditions (Clear vs Rain vs Fog) degrade appropriate sensors."""
        env_clear = generate_environment(aircraft_type=AircraftType.COMMERCIAL, weather="Clear", distance=25.0, seed=99)
        env_rain = generate_environment(aircraft_type=AircraftType.COMMERCIAL, weather="Rain", distance=25.0, seed=99)
        env_fog = generate_environment(aircraft_type=AircraftType.COMMERCIAL, weather="Fog", distance=25.0, seed=99)

        scores_clear = calculate_sensor_scores(env_clear, seed=99)
        scores_rain = calculate_sensor_scores(env_rain, seed=99)
        scores_fog = calculate_sensor_scores(env_fog, seed=99)

        # Rain degrades Radar more than Clear
        self.assertGreaterEqual(scores_clear["Radar"], scores_rain["Radar"])

        # Fog degrades Infrared and EO Camera more than Clear
        self.assertGreaterEqual(scores_clear["Infrared"], scores_fog["Infrared"])
        self.assertGreaterEqual(scores_clear["EO_Camera"], scores_fog["EO_Camera"])

    def test_electronic_jamming_impact(self):
        """Verify Electronic Jamming degrades Radar confidence."""
        env_no_jam = generate_environment(aircraft_type=AircraftType.COMMERCIAL, jamming_level=0.0, distance=20.0, seed=77)
        env_heavy_jam = generate_environment(aircraft_type=AircraftType.COMMERCIAL, jamming_level=0.9, distance=20.0, seed=77)

        scores_no_jam = calculate_sensor_scores(env_no_jam, seed=77)
        scores_heavy_jam = calculate_sensor_scores(env_heavy_jam, seed=77)

        self.assertGreater(
            scores_no_jam["Radar"],
            scores_heavy_jam["Radar"],
            "Electronic jamming should reduce radar confidence score"
        )

    def test_sensor_health_states(self):
        """Verify Offline sensor health produces 0.0 score."""
        health_cfg = {"Radar": "Offline", "Infrared": "Healthy"}
        env = generate_environment(sensor_health=health_cfg, seed=10)
        scores = calculate_sensor_scores(env, seed=10)

        self.assertEqual(scores["Radar"], 0.0, "Offline sensor must return score of 0.0")
        self.assertGreater(scores["Infrared"], 0.0, "Healthy sensor should return positive score")

    def test_distance_decay(self):
        """Verify long distance reduces detection confidence across sensors."""
        env_close = generate_environment(distance=10.0, seed=55)
        env_far = generate_environment(distance=90.0, seed=55)

        scores_close = calculate_sensor_scores(env_close, seed=55)
        scores_far = calculate_sensor_scores(env_far, seed=55)

        self.assertGreater(scores_close["Radar"], scores_far["Radar"])
        self.assertGreater(scores_close["Infrared"], scores_far["Infrared"])

    def test_deterministic_reproducibility(self):
        """Verify identical seed produces identical environment and sensor scores."""
        env1 = generate_environment(seed=12345)
        env2 = generate_environment(seed=12345)
        scores1 = calculate_sensor_scores(env1, seed=12345)
        scores2 = calculate_sensor_scores(env2, seed=12345)

        self.assertEqual(env1["distance"], env2["distance"])
        self.assertEqual(env1["aircraft_type"], env2["aircraft_type"])
        self.assertEqual(scores1["Radar"], scores2["Radar"])
        self.assertEqual(scores1["Infrared"], scores2["Infrared"])
        self.assertEqual(scores1["Acoustic"], scores2["Acoustic"])

    def test_ai_module_compatibility(self):
        """Verify ai/predict.py consumes updated sensor engine outputs without errors."""
        env = generate_environment()
        scores = calculate_sensor_scores(env)
        data = {**env, **scores}

        prediction, confidence = predict(data)
        self.assertIn(prediction, [0, 1])
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_quantum_module_compatibility(self):
        """Verify quantum/optimizer.py consumes updated sensor scores without errors."""
        env = generate_environment()
        scores = calculate_sensor_scores(env)

        selection = optimize_sensors(scores)
        self.assertIn("Radar", selection)
        self.assertIn("Infrared", selection)
        self.assertIn("Acoustic", selection)
        self.assertIsInstance(selection["Radar"], bool)

    def test_explainability_content(self):
        """Verify explanations dictionary contains bullet points for every sensor."""
        env = generate_environment()
        scores = calculate_sensor_scores(env)

        explanations = scores["explanations"]
        for sensor in ["Radar", "Infrared", "Thermal", "Acoustic", "EO_Camera"]:
            self.assertIn(sensor, explanations)
            self.assertGreater(len(explanations[sensor]), 0)


if __name__ == "__main__":
    unittest.main()
