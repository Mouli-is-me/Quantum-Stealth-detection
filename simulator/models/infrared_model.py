"""
Infrared (IR) Sensor Model
Computes IR detection confidence using Stefan-Boltzmann radiation, Beer-Lambert atmospheric extinction,
engine heat output, humidity, time of day, sensor health, and actual scenario detection distance.
"""

import math
from typing import Dict, Any, Tuple, Optional
from simulator.profiles import AircraftProfile
from simulator.environment import EnvironmentConfig, Weather, HEALTH_MULTIPLIERS
from simulator.noise import NoiseEngine


def calculate_infrared_confidence(
    profile: AircraftProfile,
    env: EnvironmentConfig,
    engine_heat: float,
    ir_emission: float,
    noise_engine: NoiseEngine
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates Infrared (IR) detection confidence [0.0, 1.0] and operational detection distance.
    """
    health_state = env.sensor_health.get("Infrared")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))

    if health_multiplier <= 0.0:
        metadata = {
            "sensor": "Infrared",
            "base_score": 0.0,
            "ir_radiance_source": 0.0,
            "ir_extinction_coef": 0.0,
            "atm_transmission": 0.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0,
            "detection_distance_km": None,
            "status": "Not Detected",
            "reason": "Sensor offline or unserviceable"
        }
        return 0.0, metadata

    dist_km = max(0.5, env.distance_km)

    # 1. Effective IR Radiance at source
    ir_source = max(0.01, engine_heat * ir_emission)

    # 2. Distance decay
    dist_factor = (15.0 / dist_km) ** 1.3

    # 3. Beer-Lambert Atmospheric Extinction
    gamma_ir = env.get_ir_extinction_coef()
    atm_transmission = math.exp(-gamma_ir * dist_km)

    # 4. Thermal Contrast against ambient environment
    temp_contrast_factor = max(0.7, 1.0 - max(0.0, env.ambient_temp_c - 20.0) * 0.008)

    # 5. Raw IR Signal Score
    raw_ir_signal = ir_source * dist_factor * atm_transmission * temp_contrast_factor * health_multiplier
    base_confidence = min(1.0, max(0.0, 1.0 - math.exp(-1.2 * raw_ir_signal)))

    # 6. Apply measurement noise
    stochastic_noise_std = 0.03 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    # 7. Calculate Actual Operational Detection Distance
    det_dist_km, status, reason = _calculate_ir_detection_distance(
        ir_source=ir_source,
        gamma_ir=gamma_ir,
        env=env,
        health_multiplier=health_multiplier,
        final_score=final_score
    )

    metadata = {
        "sensor": "Infrared",
        "base_score": round(base_confidence, 3),
        "ir_radiance_source": round(ir_source, 3),
        "ir_extinction_coef": round(gamma_ir, 4),
        "atm_transmission": round(atm_transmission, 3),
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4),
        "detection_distance_km": det_dist_km,
        "status": status,
        "reason": reason
    }

    return final_score, metadata


def _calculate_ir_detection_distance(
    ir_source: float,
    gamma_ir: float,
    env: EnvironmentConfig,
    health_multiplier: float,
    final_score: float
) -> Tuple[Optional[float], str, str]:
    """Calculates operational infrared detection range under current atmospheric conditions."""
    if health_multiplier <= 0.0 or final_score < 0.20:
        if env.weather in [Weather.MORNING_FOG, Weather.DENSE_FOG, Weather.FOG, Weather.NIGHT_FOG]:
            reason_str = "IR signal scattered by dense fog"
        elif env.humidity_pct > 80:
            reason_str = "High humidity atmospheric extinction"
        else:
            reason_str = "IR signature below sensor sensitivity threshold"
        return None, "Not Detected", reason_str

    base_range = 28.0 * (ir_source ** 0.45) * (health_multiplier ** 0.5)
    attenuation_factor = 1.0 + (gamma_ir * 12.0)
    det_dist = max(0.8, base_range / attenuation_factor)
    det_dist = round(det_dist, 1)

    reasons = []
    if env.weather in [Weather.MORNING_FOG, Weather.DENSE_FOG, Weather.FOG, Weather.NIGHT_FOG]:
        reasons.append("fog extinction")
    elif env.weather in [Weather.HEAVY_RAIN, Weather.THUNDERSTORM, Weather.HEAVY_SNOW]:
        reasons.append("precipitation scattering")
    if env.humidity_pct > 75:
        reasons.append("high humidity")
    if ir_source < 0.2:
        reasons.append("engine thermal masking")

    if reasons:
        reason_str = f"Attenuated by {', '.join(reasons)}"
    else:
        reason_str = "Clear atmospheric IR transmission"

    return det_dist, "Detected", reason_str
