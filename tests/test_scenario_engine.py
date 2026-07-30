"""
Unit and Integration Tests for Scenario Intelligence Engine (Part 2)
Verifies mission templates, validation rules, demo scenarios, multi-target generation, ground truth,
and backward compatibility with AI and Quantum modules.
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), ".."))))

from simulator.scenario_engine import ScenarioEngine
from simulator.missions import MissionType, MISSION_TEMPLATES
from simulator.profiles import AircraftType, PROFILES
from simulator.validation import ScenarioValidator
from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from ai.predict import predict
from quantum.optimizer import optimize_sensors


class TestScenarioEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ScenarioEngine(seed=42)

    def test_mission_templates_coverage(self):
        """Verify all 12 mission templates are defined and accessible."""
        self.assertEqual(len(MISSION_TEMPLATES), 12)
        for mission_enum in MissionType:
            self.assertIn(mission_enum, MISSION_TEMPLATES)
            template = MISSION_TEMPLATES[mission_enum]
            self.assertIsNotNone(template.name)
            self.assertGreater(len(template.primary_aircraft_types), 0)

    def test_physical_validation_rules(self):
        """Verify ScenarioValidator flags impossible physical combinations."""
        profile = PROFILES[AircraftType.BIRD]
        
        # Impossible bird at 12,000m altitude and 120 dB acoustic noise
        is_valid, violations = ScenarioValidator.validate_target_physics(
            profile, speed_knots=30.0, altitude_m=12000.0, rcs_m2=0.01, stealth_rating=0.95, acoustic_spl_db=120.0
        )
        self.assertFalse(is_valid, "Validator should reject bird at 12,000m with 120 dB noise")
        self.assertGreater(len(violations), 0)

        # Auto-correction
        c = ScenarioValidator.auto_correct_target_parameters(
            profile, speed_knots=30.0, altitude_m=12000.0, rcs_m2=0.01, stealth_rating=0.95, acoustic_spl_db=120.0
        )
        self.assertLessEqual(c["altitude_m"], profile.altitude_range_m[1])
        self.assertLessEqual(c["acoustic_spl_db"], profile.acoustic_spl_range_db[1])

    def test_demo_presets_1_to_8(self):
        """Verify all 8 predefined demonstration scenario presets generate deterministically."""
        for preset_id in range(1, 9):
            scen = self.engine.generate_demo_scenario(preset_id)
            self.assertEqual(scen.scenario_id, f"DEMO-{preset_id:03d}")
            self.assertIsNotNone(scen.primary_target)
            self.assertIn("ground_truth", scen.scenario_metadata)
            self.assertIn("difficulty_level", scen.scenario_metadata)

    def test_multi_target_generation(self):
        """Verify multi-target scenario generation with target_count > 1."""
        scen = self.engine.generate_scenario(target_count=4, seed=999)
        self.assertEqual(scen.total_targets, 4)
        self.assertEqual(len(scen.secondary_targets), 3)
        self.assertTrue(scen.primary_target.is_primary)
        for sec in scen.secondary_targets:
            self.assertFalse(sec.is_primary)

    def test_ground_truth_and_metadata(self):
        """Verify ground truth structure and scenario metadata completeness."""
        scen = self.engine.generate_scenario(seed=777)
        gt = scen.scenario_metadata["ground_truth"]

        self.assertIn("true_aircraft_class", gt)
        self.assertIn("threat_category", gt)
        self.assertIn("threat_detected", gt)
        self.assertIn("expected_sensor_strengths", gt)
        self.assertIn("expected_sensor_weaknesses", gt)
        self.assertIn("expected_fusion_confidence", gt)

        self.assertIn("scenario_id", scen.scenario_metadata)
        self.assertIn("difficulty_level", scen.scenario_metadata)
        self.assertIn("timestamp", scen.scenario_metadata)

    def test_facade_backward_compatibility_with_presets(self):
        """Verify generate_environment with demo_preset maintains full backward compatibility."""
        env = generate_environment(demo_preset=4)  # Cruise missile under jamming
        self.assertIn("distance", env)
        self.assertIn("weather", env)
        self.assertIn("stealth", env)
        self.assertIn("engine_heat", env)
        self.assertIn("noise", env)
        self.assertEqual(env["aircraft_type"], "Cruise Missile")

        scores = calculate_sensor_scores(env)
        self.assertIn("Radar", scores)
        self.assertIn("Infrared", scores)
        self.assertIn("Acoustic", scores)

        # AI and Quantum integration test
        pred, conf = predict({**env, **scores})
        self.assertIn(pred, [0, 1])
        
        selection = optimize_sensors(scores)
        self.assertIn("Radar", selection)


if __name__ == "__main__":
    unittest.main()
