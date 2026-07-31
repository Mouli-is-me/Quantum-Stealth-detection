"""
Research-Grade Physics-Inspired Synthetic Sensor Simulator & Scenario Engine Facade
Provides generate_environment and calculate_sensor_scores with 100% backward compatibility.
"""

from typing import Dict, Any, Optional, Union

from simulator.profiles import AircraftType, AircraftProfile, get_profile
from simulator.environment import (
    EnvironmentConfig, Weather, SensorHealth, parse_weather, parse_sensor_health
)
from simulator.missions import MissionType, get_mission_template
from simulator.scenario_engine import ScenarioEngine
from simulator.noise import NoiseEngine
from simulator.models.radar_model import calculate_radar_confidence
from simulator.models.infrared_model import calculate_infrared_confidence
from simulator.models.thermal_model import calculate_thermal_confidence
from simulator.models.acoustic_model import calculate_acoustic_confidence
from simulator.models.eo_camera_model import calculate_eo_camera_confidence
from simulator.explainability import generate_sensor_explanations


def normalize_legacy_weather(w: Weather) -> str:
    """Maps extended Weather enum to legacy 3-category weather string ('Clear', 'Rain', 'Fog')."""
    if w in [Weather.CLEAR, Weather.CLEAR_DAY, Weather.NIGHT, Weather.DESERT_HEAT]:
        return "Clear"
    elif w in [Weather.RAIN, Weather.HEAVY_RAIN, Weather.SNOW]:
        return "Rain"
    else:  # Weather.FOG, Weather.CLOUDY, Weather.MOUNTAIN_REGION, Weather.ELECTRONIC_JAMMING
        return "Fog"


def generate_environment(
    aircraft_type: Optional[Union[str, AircraftType]] = None,
    weather: Optional[Union[str, Weather]] = None,
    distance: Optional[float] = None,
    seed: Optional[int] = None,
    jamming_level: Optional[float] = None,
    sensor_health: Optional[Dict[str, Union[str, SensorHealth]]] = None,
    mission_type: Optional[Union[str, MissionType]] = None,
    demo_preset: Optional[int] = None,
    target_count: int = 1
) -> Dict[str, Any]:
    """
    Generates a simulated operational battlefield environment & target scenario.
    
    100% Backward Compatible Return Dict:
    Contains all legacy keys:
      - 'distance': float (5 to 100 km)
      - 'weather': str ('Clear', 'Rain', 'Fog')
      - 'stealth': float [0.0, 1.0]
      - 'engine_heat': float [0.0, 1.0]
      - 'noise': float [0.0, 1.0]
    Plus extended Scenario Intelligence & Ground Truth metadata.
    """
    engine = ScenarioEngine(seed=seed)

    if demo_preset is not None and 1 <= demo_preset <= 8:
        multi_scenario = engine.generate_demo_scenario(demo_preset)
    else:
        multi_scenario = engine.generate_scenario(
            mission_type=mission_type,
            aircraft_type=aircraft_type,
            weather=weather,
            distance_km=distance,
            jamming_level=jamming_level,
            target_count=target_count,
            sensor_health=sensor_health,
            seed=seed
        )

    primary_tgt = multi_scenario.primary_target
    env_cfg = multi_scenario.environment
    meta = multi_scenario.scenario_metadata

    # Normalized legacy mapping
    engine_heat_legacy = round(max(0.0, min(1.0, (primary_tgt.ir_emission + (primary_tgt.thermal_delta_c / 60.0)) / 2.0)), 3)
    noise_legacy = round(max(0.0, min(1.0, (primary_tgt.acoustic_spl_db - 40.0) / 100.0)), 3)
    stealth_legacy = round(max(0.0, min(1.0, primary_tgt.stealth_rating)), 3)

    legacy_weather = normalize_legacy_weather(env_cfg.weather)

    return {
        # --- LEGACY KEYS (DO NOT MODIFY NAMES OR FORMATS) ---
        "distance": round(primary_tgt.distance_km, 1),
        "weather": legacy_weather,
        "stealth": stealth_legacy,
        "engine_heat": engine_heat_legacy,
        "noise": noise_legacy,

        # --- EXTENDED SCENARIO INTELLIGENCE & METADATA ---
        "scenario_id": multi_scenario.scenario_id,
        "weather_detailed": env_cfg.weather.value,
        "aircraft_type": primary_tgt.profile.name,
        "speed": round(primary_tgt.speed_knots, 1),
        "altitude": round(primary_tgt.altitude_m, 1),
        "heading": round(primary_tgt.heading_deg, 1),
        "temperature": round(env_cfg.ambient_temp_c, 1),
        "humidity": round(env_cfg.humidity_pct, 1),
        "visibility": round(env_cfg.visibility_km, 1),
        "jamming": round(env_cfg.jamming_level, 2),
        "sensor_health": {k: v.value for k, v in env_cfg.sensor_health.items()},
        "mission_type": env_cfg.mission_type.value if hasattr(env_cfg.mission_type, "value") else str(env_cfg.mission_type),
        "target_count": multi_scenario.total_targets,
        "difficulty_level": meta.get("difficulty_level", "Medium"),
        "threat_level": meta.get("threat_level", "Medium"),
        "ground_truth": meta.get("ground_truth", {}),
        "targets": [t.to_dict() for t in multi_scenario.get_all_targets()],

        # Internal Physical Variables
        "_rcs_m2": primary_tgt.rcs_m2,
        "_ir_emission": primary_tgt.ir_emission,
        "_thermal_delta_c": primary_tgt.thermal_delta_c,
        "_acoustic_spl_db": primary_tgt.acoustic_spl_db,
        "_visual_contrast": primary_tgt.visual_contrast,
        "_seed": seed,
        "_env_config": env_cfg,
        "_profile": primary_tgt.profile,
        "_multi_scenario": multi_scenario
    }


def calculate_sensor_scores(
    env: Dict[str, Any],
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Calculates confidence scores for each sensor modality using physics engines.
    
    100% Backward Compatible Return Dict:
    Top-level keys 'Radar', 'Infrared', and 'Acoustic' contain float values [0.0, 1.0].
    Also includes 'Thermal', 'EO_Camera', and diagnostic explainability metadata.
    """
    if "_env_config" in env:
        env_config: EnvironmentConfig = env["_env_config"]
    else:
        dist = float(env.get("distance", 25.0))
        weath = parse_weather(env.get("weather_detailed", env.get("weather", "Clear")))
        jam = float(env.get("jamming", 0.0))
        health_raw = env.get("sensor_health", {})
        health_dict = {
            "Radar": parse_sensor_health(health_raw.get("Radar", "Healthy")),
            "Infrared": parse_sensor_health(health_raw.get("Infrared", "Healthy")),
            "Thermal": parse_sensor_health(health_raw.get("Thermal", "Healthy")),
            "Acoustic": parse_sensor_health(health_raw.get("Acoustic", "Healthy")),
            "EO_Camera": parse_sensor_health(health_raw.get("EO_Camera", "Healthy")),
        }
        env_config = EnvironmentConfig(
            distance_km=dist,
            weather=weath,
            jamming_level=jam,
            sensor_health=health_dict
        )

    if "_profile" in env:
        profile: AircraftProfile = env["_profile"]
    else:
        profile = get_profile(env.get("aircraft_type", "Unknown Object"))

    calc_seed = seed if seed is not None else env.get("_seed", None)
    noise_engine = NoiseEngine(seed=calc_seed)

    rcs_m2 = env.get("_rcs_m2", 1.0)
    stealth = env.get("stealth", profile.stealth_rating_range[0])
    ir_emission = env.get("_ir_emission", 0.5)
    engine_heat = env.get("engine_heat", 0.5)
    speed_knots = env.get("speed", 300.0)
    thermal_delta = env.get("_thermal_delta_c", 25.0)
    acoustic_spl = env.get("_acoustic_spl_db", 85.0)
    noise_factor = env.get("noise", 0.5)
    visual_contrast = env.get("_visual_contrast", 0.5)

    radar_score, radar_meta = calculate_radar_confidence(
        profile, env_config, rcs_m2, stealth, noise_engine
    )

    ir_score, ir_meta = calculate_infrared_confidence(
        profile, env_config, engine_heat, ir_emission, noise_engine
    )

    thermal_score, thermal_meta = calculate_thermal_confidence(
        profile, env_config, speed_knots, thermal_delta, engine_heat, noise_engine
    )

    acoustic_score, acoustic_meta = calculate_acoustic_confidence(
        profile, env_config, acoustic_spl, noise_factor, noise_engine
    )

    eo_score, eo_meta = calculate_eo_camera_confidence(
        profile, env_config, visual_contrast, noise_engine
    )

    scores_dict = {
        "Radar": radar_score,
        "Infrared": ir_score,
        "Thermal": thermal_score,
        "Acoustic": acoustic_score,
        "EO_Camera": eo_score
    }

    metadata_dict = {
        "Radar": radar_meta,
        "Infrared": ir_meta,
        "Thermal": thermal_meta,
        "Acoustic": acoustic_meta,
        "EO_Camera": eo_meta
    }

    target_info = {
        "aircraft_type": profile.name,
        "stealth": stealth,
        "engine_heat": engine_heat
    }

    explanations = generate_sensor_explanations(
        env_config, scores_dict, metadata_dict, target_info
    )

    return {
        "Radar": radar_score,
        "Infrared": ir_score,
        "Acoustic": acoustic_score,
        "Thermal": thermal_score,
        "EO_Camera": eo_score,
        "explanations": explanations,
        "metadata": metadata_dict,
        "sensor_health": {k: v.value for k, v in env_config.sensor_health.items()},
        "ground_truth": env.get("ground_truth", {})
    }