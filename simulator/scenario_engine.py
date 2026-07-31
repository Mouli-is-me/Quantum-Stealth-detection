"""
Scenario Engine Module
Orchestrates mission templates, aircraft profiles, physical validation, multi-target generation,
ground truth calculation, and scenario metadata generation.
"""

import time
import uuid
import random
from typing import Dict, Any, Optional, List, Union

from simulator.profiles import AircraftType, AircraftProfile, get_profile, PROFILES
from simulator.environment import EnvironmentConfig, Weather, SensorHealth, parse_weather, parse_sensor_health
from simulator.missions import MissionType, MissionTemplate, ThreatLevel, get_mission_template
from simulator.multi_target import TargetState, MultiTargetScenario
from simulator.validation import ScenarioValidator
from simulator.demo_scenarios import get_demo_preset, DEMO_SCENARIO_PRESETS
from simulator.noise import NoiseEngine


class ScenarioEngine:
    """Core intelligence engine driving realistic scenario generation."""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.noise_engine = NoiseEngine(seed=seed)

    def set_seed(self, seed: Optional[int]) -> None:
        self.seed = seed
        self.noise_engine.reseed(seed)

    def generate_scenario(
        self,
        mission_type: Optional[Union[str, MissionType]] = None,
        aircraft_type: Optional[Union[str, AircraftType]] = None,
        weather: Optional[Union[str, Weather]] = None,
        distance_km: Optional[float] = None,
        jamming_level: Optional[float] = None,
        target_count: int = 1,
        sensor_health: Optional[Dict[str, Union[str, SensorHealth]]] = None,
        seed: Optional[int] = None
    ) -> MultiTargetScenario:
        """Generates a complete, validated operational scenario."""
        if seed is not None:
            self.set_seed(seed)

        py_rng = self.noise_engine._python_rng

        # 1. Mission Selection
        if mission_type is None:
            selected_mission_enum = py_rng.choice(list(MissionType))
        else:
            selected_mission_enum = mission_type

        mission_template = get_mission_template(selected_mission_enum)

        # 2. Primary Aircraft Selection
        if aircraft_type is None:
            selected_aircraft_type = py_rng.choice(mission_template.primary_aircraft_types)
        else:
            selected_aircraft_type = aircraft_type

        primary_profile = get_profile(selected_aircraft_type)

        # 3. Environment & Atmospheric Settings
        if weather is None:
            selected_weather = py_rng.choice(list(Weather))
        else:
            selected_weather = parse_weather(weather)

        if distance_km is not None:
            dist = float(distance_km)
        else:
            dist = py_rng.uniform(5.0, 95.0)

        if jamming_level is not None:
            jam = max(0.0, min(1.0, float(jamming_level)))
        else:
            if selected_weather == Weather.ELECTRONIC_JAMMING:
                jam = py_rng.uniform(0.5, 0.95)
            else:
                jam = py_rng.choice([0.0, 0.0, 0.1, 0.4])

        # Health setup
        health_dict = {
            "Radar": SensorHealth.HEALTHY,
            "Infrared": SensorHealth.HEALTHY,
            "Thermal": SensorHealth.HEALTHY,
            "Acoustic": SensorHealth.HEALTHY,
            "EO_Camera": SensorHealth.HEALTHY,
        }
        if sensor_health is not None:
            for s_name, s_val in sensor_health.items():
                if s_name in health_dict:
                    health_dict[s_name] = parse_sensor_health(s_val)

        env_config = EnvironmentConfig(
            distance_km=dist,
            weather=selected_weather,
            ambient_temp_c=py_rng.uniform(-5.0, 35.0),
            humidity_pct=py_rng.uniform(30.0, 95.0),
            visibility_km=py_rng.uniform(2.0, 25.0),
            jamming_level=jam,
            heading_deg=py_rng.uniform(0.0, 360.0),
            mission_type=mission_template.mission_type,
            sensor_health=health_dict
        )

        # 4. Generate Primary Target Parameters
        raw_speed = py_rng.uniform(*primary_profile.speed_range_knots)
        raw_alt = py_rng.uniform(*primary_profile.altitude_range_m)
        raw_rcs = py_rng.uniform(*primary_profile.rcs_range_m2)
        raw_stealth = py_rng.uniform(*primary_profile.stealth_rating_range)
        raw_spl = py_rng.uniform(*primary_profile.acoustic_spl_range_db)

        # Validate & Auto-correct Primary Target
        corrected_params = ScenarioValidator.auto_correct_target_parameters(
            primary_profile, raw_speed, raw_alt, raw_rcs, raw_stealth, raw_spl
        )

        primary_target = TargetState(
            target_id="TGT-001",
            aircraft_type=primary_profile.aircraft_type,
            profile=primary_profile,
            distance_km=dist,
            heading_deg=env_config.heading_deg,
            speed_knots=corrected_params["speed_knots"],
            altitude_m=corrected_params["altitude_m"],
            rcs_m2=corrected_params["rcs_m2"],
            ir_emission=py_rng.uniform(*primary_profile.ir_emission_range),
            thermal_delta_c=py_rng.uniform(*primary_profile.thermal_delta_range_c),
            acoustic_spl_db=corrected_params["acoustic_spl_db"],
            visual_contrast=py_rng.uniform(*primary_profile.visual_contrast_range),
            stealth_rating=corrected_params["stealth_rating"],
            is_primary=True,
            threat_category=primary_profile.threat_category
        )

        # 5. Multi-Target Generation (Secondary targets if count > 1)
        secondary_targets: List[TargetState] = []
        for i in range(2, max(1, target_count) + 1):
            sec_type = py_rng.choice([AircraftType.RECON_DRONE, AircraftType.BIRD, AircraftType.COMMERCIAL])
            sec_profile = get_profile(sec_type)
            sec_speed = py_rng.uniform(*sec_profile.speed_range_knots)
            sec_alt = py_rng.uniform(*sec_profile.altitude_range_m)
            sec_rcs = py_rng.uniform(*sec_profile.rcs_range_m2)
            sec_stealth = py_rng.uniform(*sec_profile.stealth_rating_range)
            sec_spl = py_rng.uniform(*sec_profile.acoustic_spl_range_db)

            c_sec = ScenarioValidator.auto_correct_target_parameters(
                sec_profile, sec_speed, sec_alt, sec_rcs, sec_stealth, sec_spl
            )

            sec_tgt = TargetState(
                target_id=f"TGT-{i:03d}",
                aircraft_type=sec_profile.aircraft_type,
                profile=sec_profile,
                distance_km=dist + py_rng.uniform(-3.0, 5.0),
                heading_deg=(env_config.heading_deg + py_rng.uniform(-20.0, 20.0)) % 360.0,
                speed_knots=c_sec["speed_knots"],
                altitude_m=c_sec["altitude_m"],
                rcs_m2=c_sec["rcs_m2"],
                ir_emission=py_rng.uniform(*sec_profile.ir_emission_range),
                thermal_delta_c=py_rng.uniform(*sec_profile.thermal_delta_range_c),
                acoustic_spl_db=c_sec["acoustic_spl_db"],
                visual_contrast=py_rng.uniform(*sec_profile.visual_contrast_range),
                stealth_rating=c_sec["stealth_rating"],
                is_primary=False,
                threat_category=sec_profile.threat_category
            )
            secondary_targets.append(sec_tgt)

        # 6. Scenario Difficulty & Ground Truth Calculation
        difficulty = self._calculate_difficulty(primary_profile, env_config, jam, target_count)
        ground_truth = self._calculate_ground_truth(primary_target, env_config, mission_template)

        scenario_id = f"SCEN-{uuid.uuid4().hex[:8].upper()}"

        metadata = {
            "scenario_id": scenario_id,
            "mission_name": mission_template.name,
            "mission_type": mission_template.mission_type.value,
            "weather": selected_weather.value,
            "threat_level": mission_template.threat_level.value,
            "difficulty_level": difficulty,
            "target_count": 1 + len(secondary_targets),
            "random_seed": self.seed,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "ground_truth": ground_truth
        }

        return MultiTargetScenario(
            scenario_id=scenario_id,
            primary_target=primary_target,
            secondary_targets=secondary_targets,
            environment=env_config,
            scenario_metadata=metadata
        )

    def generate_demo_scenario(self, preset_id: int) -> MultiTargetScenario:
        """Generates a predefined, deterministic demonstration scenario (presets 1..8)."""
        preset = get_demo_preset(preset_id)
        scen = self.generate_scenario(
            mission_type=preset.get("mission_type"),
            aircraft_type=preset.get("aircraft_type"),
            weather=preset.get("weather"),
            distance_km=preset.get("distance_km"),
            jamming_level=preset.get("jamming_level", 0.0),
            target_count=preset.get("target_count", 1),
            sensor_health=preset.get("sensor_health"),
            seed=preset.get("seed")
        )

        scen.scenario_id = preset["scenario_id"]
        scen.scenario_metadata["scenario_id"] = preset["scenario_id"]
        scen.scenario_metadata["demo_title"] = preset["title"]
        scen.scenario_metadata["demo_description"] = preset["description"]
        return scen

    def _calculate_difficulty(
        self,
        profile: AircraftProfile,
        env: EnvironmentConfig,
        jamming: float,
        target_count: int
    ) -> str:

        score = 0.0
        score += profile.stealth_rating_range[1] * 3.5
        score += (env.distance_km / 100.0) * 2.0
        score += jamming * 3.5
        if env.weather in [Weather.HEAVY_RAIN, Weather.DENSE_FOG, Weather.THUNDERSTORM, Weather.HEAVY_SNOW, Weather.SANDSTORM]:
            score += 2.5
        elif env.weather in [Weather.LIGHT_RAIN, Weather.MORNING_FOG, Weather.SNOW, Weather.HAZE]:
            score += 1.2
        if target_count > 1:
            score += target_count * 0.8

        if score < 1.5:
            return "Very Easy"
        elif score < 3.0:
            return "Easy"
        elif score < 4.2:
            return "Normal"
        elif score < 5.5:
            return "Moderate"
        elif score < 6.8:
            return "Hard"
        elif score < 8.0:
            return "Very Hard"
        elif score < 9.2:
            return "Extreme"
        elif score < 10.5:
            return "Combat"
        elif score < 12.0:
            return "Hostile"
        else:
            return "Maximum Threat"

    def _calculate_ground_truth(
        self,
        target: TargetState,
        env: EnvironmentConfig,
        mission: MissionTemplate
    ) -> Dict[str, Any]:

        strengths = []
        weaknesses = []

        if target.rcs_m2 > 5.0 and target.stealth_rating < 0.2:
            strengths.append("Radar")
        else:
            weaknesses.append("Radar")

        if target.ir_emission > 0.6:
            strengths.append("Infrared")
        else:
            weaknesses.append("Infrared")

        if target.speed_knots > 450:
            strengths.append("Thermal")

        if target.acoustic_spl_db > 100 and env.distance_km < 20:
            strengths.append("Acoustic")
        else:
            weaknesses.append("Acoustic")

        if env.get_optical_visibility_km() > 15.0 and target.visual_contrast > 0.6:
            strengths.append("EO_Camera")
        else:
            weaknesses.append("EO_Camera")

        is_threat = target.threat_category in ["MILITARY_STRIKE", "RECON"] or mission.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]

        return {
            "true_aircraft_class": target.aircraft_type.value,
            "threat_category": target.threat_category,
            "threat_detected": is_threat,
            "expected_sensor_strengths": strengths,
            "expected_sensor_weaknesses": weaknesses,
            "expected_fusion_confidence": 0.85 if len(strengths) >= 2 else 0.40
        }
