"""
Electro-Optical (EO) Camera Model
Computes visual detection confidence using Koschmieder optical contrast transmittance,
visibility range, solar illuminance, weather extinction, camera health, and actual scenario detection distance.
"""

import math
from typing import Dict, Any, Tuple, Optional
from simulator.profiles import AircraftProfile
from simulator.environment import EnvironmentConfig, Weather, HEALTH_MULTIPLIERS
from simulator.noise import NoiseEngine


def calculate_eo_camera_confidence(
    profile: AircraftProfile,
    env: EnvironmentConfig,
    visual_contrast: float,
    noise_engine: NoiseEngine
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates Electro-Optical (EO) Camera detection confidence [0.0, 1.0] and operational detection distance.
    """
    health_state = env.sensor_health.get("EO_Camera")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))

    if health_multiplier <= 0.0:
        metadata = {
            "sensor": "EO_Camera",
            "base_score": 0.0,
            "inherent_contrast": 0.0,
            "visibility_km": 0.0,
            "extinction_coef_sigma": 0.0,
            "apparent_contrast": 0.0,
            "solar_illuminance_factor": 0.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0,
            "detection_distance_km": None,
            "status": "Not Detected",
            "reason": "Sensor offline or unserviceable"
        }
        return 0.0, metadata

    dist_km = max(0.2, env.distance_km)
    vis_km = max(0.1, env.get_optical_visibility_km())

    # 1. Atmospheric Optical Extinction Coefficient (Koschmieder law)
    sigma_vis = 3.912 / vis_km
    apparent_contrast = visual_contrast * math.exp(-sigma_vis * dist_km)

    # 2. Solar Illuminance Factor (Day vs Night lighting)
    if env.weather in [Weather.NIGHT, Weather.NIGHT_FOG]:
        solar_illuminance = 0.15  # Night low light
    elif env.weather in [Weather.CLOUDY, Weather.THUNDERSTORM, Weather.DENSE_FOG, Weather.SMOKE]:
        solar_illuminance = 0.50  # Low ambient light
    else:
        solar_illuminance = 1.00  # Daylight

    # 3. Geometric Optical Resolution
    resolution_decay = (15.0 / dist_km) ** 1.2

    # 4. Total Optical Signal Factor
    optical_signal = apparent_contrast * solar_illuminance * resolution_decay * health_multiplier
    base_confidence = min(1.0, max(0.0, 1.0 - math.exp(-1.5 * optical_signal)))

    # 5. Apply measurement noise
    stochastic_noise_std = 0.035 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    # 6. Calculate Actual Operational Detection Distance
    det_dist_km, status, reason = _calculate_eo_detection_distance(
        vis_km=vis_km,
        visual_contrast=visual_contrast,
        solar_illuminance=solar_illuminance,
        env=env,
        health_multiplier=health_multiplier,
        final_score=final_score
    )

    metadata = {
        "sensor": "EO_Camera",
        "base_score": round(base_confidence, 3),
        "inherent_contrast": round(visual_contrast, 3),
        "visibility_km": round(vis_km, 2),
        "extinction_coef_sigma": round(sigma_vis, 4),
        "apparent_contrast": round(apparent_contrast, 4),
        "solar_illuminance_factor": solar_illuminance,
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4),
        "detection_distance_km": det_dist_km,
        "status": status,
        "reason": reason
    }

    return final_score, metadata


def _calculate_eo_detection_distance(
    vis_km: float,
    visual_contrast: float,
    solar_illuminance: float,
    env: EnvironmentConfig,
    health_multiplier: float,
    final_score: float
) -> Tuple[Optional[float], str, str]:
    """Calculates operational visual optical camera detection range."""
    if health_multiplier <= 0.0 or final_score < 0.20 or vis_km < 1.5 or solar_illuminance < 0.2:
        if vis_km < 2.0:
            reason_str = "Visibility below operational threshold"
        elif solar_illuminance < 0.25:
            reason_str = "Night illumination below visual sensor threshold"
        else:
            reason_str = "Optical contrast degraded by atmospheric haze"
        return None, "Not Detected", reason_str

    base_range = min(vis_km * 0.85, 22.0) * (visual_contrast ** 0.5) * (solar_illuminance ** 0.4) * (health_multiplier ** 0.5)
    det_dist = round(max(0.5, base_range), 1)

    reasons = []
    if vis_km < 8.0:
        reasons.append(f"restricted visibility ({vis_km:.1f}km)")
    if solar_illuminance < 0.6:
        reasons.append("overcast/low light")
    if visual_contrast < 0.3:
        reasons.append("low target visual contrast")

    if reasons:
        reason_str = f"Limited by {', '.join(reasons)}"
    else:
        reason_str = "High visual resolution and optimal daylight contrast"

    return det_dist, "Detected", reason_str
