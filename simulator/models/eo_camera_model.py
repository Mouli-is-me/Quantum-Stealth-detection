"""
Electro-Optical (EO) Camera Model
Computes visual detection confidence using Koschmieder optical contrast transmittance,
visibility range, solar illuminance, weather extinction, and camera health.
"""

import math
from typing import Dict, Any, Tuple
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
    Calculates Electro-Optical (EO) Camera detection confidence [0.0, 1.0].
    
    Physics Model:
    1. Koschmieder Optical Contrast Transmittance: C(R) = C_0 * exp(-sigma_vis * distance_km)
       where extinction coefficient sigma_vis = 3.912 / visibility_km
    2. Solar Illuminance Factor (Day vs Night)
    3. Weather attenuation (Fog, Rain, Snow)
    4. Distance resolution decay: (15 / R)^1.2
    5. Camera Sensor Health & Noise
    """
    health_state = env.sensor_health.get("EO_Camera")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))

    if health_multiplier <= 0.0:
        return 0.0, {
            "sensor": "EO_Camera",
            "base_score": 0.0,
            "inherent_contrast": 0.0,
            "visibility_km": 0.0,
            "extinction_coef_sigma": 0.0,
            "apparent_contrast": 0.0,
            "solar_illuminance_factor": 0.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0
        }

    dist_km = max(0.2, env.distance_km)
    vis_km = max(0.1, env.get_optical_visibility_km())

    # 1. Atmospheric Optical Extinction Coefficient (Koschmieder law)
    sigma_vis = 3.912 / vis_km
    apparent_contrast = visual_contrast * math.exp(-sigma_vis * dist_km)

    # 2. Solar Illuminance Factor (Day vs Night lighting)
    if env.weather == Weather.NIGHT:
        solar_illuminance = 0.15  # Low light ambient night reduction
    else:
        solar_illuminance = 1.00  # Daylight

    # 3. Geometric Optical Resolution / Range decay
    resolution_decay = (15.0 / dist_km) ** 1.2

    # 4. Total Optical Signal Factor
    optical_signal = apparent_contrast * solar_illuminance * resolution_decay * health_multiplier

    # Map to [0.0, 1.0] using smooth sat curve
    base_confidence = min(1.0, max(0.0, 1.0 - math.exp(-1.5 * optical_signal)))

    # 5. Apply measurement noise
    stochastic_noise_std = 0.035 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    metadata = {
        "sensor": "EO_Camera",
        "base_score": round(base_confidence, 3),
        "inherent_contrast": round(visual_contrast, 3),
        "visibility_km": round(vis_km, 2),
        "extinction_coef_sigma": round(sigma_vis, 4),
        "apparent_contrast": round(apparent_contrast, 4),
        "solar_illuminance_factor": solar_illuminance,
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4)
    }

    return final_score, metadata
