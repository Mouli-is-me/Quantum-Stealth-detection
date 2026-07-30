"""
Infrared (IR) Sensor Model
Computes IR detection confidence using Stefan-Boltzmann radiation, Beer-Lambert atmospheric extinction,
engine heat output, and sensor health.
"""

import math
from typing import Dict, Any, Tuple
from simulator.profiles import AircraftProfile
from simulator.environment import EnvironmentConfig, HEALTH_MULTIPLIERS
from simulator.noise import NoiseEngine


def calculate_infrared_confidence(
    profile: AircraftProfile,
    env: EnvironmentConfig,
    engine_heat: float,
    ir_emission: float,
    noise_engine: NoiseEngine
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates Infrared (IR) detection confidence [0.0, 1.0].
    
    Physics Model:
    1. IR Radiance Source = engine_heat * ir_emission
    2. Atmospheric Extinction loss = exp(-gamma_ir * distance_km) (Beer-Lambert law)
    3. Inverse-square distance decay: (10 / R)^1.5
    4. Sensor Health Multiplier
    5. Stochastic noise
    """
    health_state = env.sensor_health.get("Infrared")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))

    if health_multiplier <= 0.0:
        return 0.0, {
            "sensor": "Infrared",
            "base_score": 0.0,
            "ir_radiance_source": 0.0,
            "ir_extinction_coef": 0.0,
            "atm_transmission": 0.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0
        }

    dist_km = max(0.5, env.distance_km)

    # 1. Effective IR Radiance at source
    ir_source = max(0.01, engine_heat * ir_emission)

    # 2. Distance decay (1-way optical energy propagation: ~R^-1.5 to R^-2)
    dist_factor = (15.0 / dist_km) ** 1.3

    # 3. Beer-Lambert Atmospheric Extinction
    gamma_ir = env.get_ir_extinction_coef()
    atm_transmission = math.exp(-gamma_ir * dist_km)

    # 4. Thermal Contrast against ambient environment
    # Higher ambient temperature reduces thermal contrast delta
    temp_contrast_factor = max(0.7, 1.0 - max(0.0, env.ambient_temp_c - 20.0) * 0.008)

    # 5. Raw IR Signal Score
    raw_ir_signal = ir_source * dist_factor * atm_transmission * temp_contrast_factor * health_multiplier

    # Map to [0.0, 1.0] using smooth sat function
    base_confidence = min(1.0, max(0.0, 1.0 - math.exp(-1.2 * raw_ir_signal)))

    # 6. Apply measurement noise
    stochastic_noise_std = 0.03 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    metadata = {
        "sensor": "Infrared",
        "base_score": round(base_confidence, 3),
        "ir_radiance_source": round(ir_source, 3),
        "ir_extinction_coef": round(gamma_ir, 4),
        "atm_transmission": round(atm_transmission, 3),
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4)
    }

    return final_score, metadata
