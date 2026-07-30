"""
Radar Sensor Model
Computes radar detection confidence using the Radar Range Equation, RCS, atmospheric attenuation,
stealth factors, electronic jamming, and sensor health.
"""

import math
from typing import Dict, Any, Tuple
from simulator.profiles import AircraftProfile
from simulator.environment import EnvironmentConfig, HEALTH_MULTIPLIERS
from simulator.noise import NoiseEngine


def calculate_radar_confidence(
    profile: AircraftProfile,
    env: EnvironmentConfig,
    rcs_m2: float,
    stealth_rating: float,
    noise_engine: NoiseEngine
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates Radar detection confidence [0.0, 1.0].
    
    Physics Model:
    1. Effective RCS = rcs_m2 * (1.0 - stealth_rating * 0.95)
    2. Free Space Path Loss ~ R^-4 (2-way radar propagation)
    3. Atmospheric RF Attenuation Loss (dB) = attenuation_db_per_km * distance_km
    4. Jamming Factor = 1.0 + 12.0 * (env.jamming_level ^ 1.5)
    5. Sensor Health Multiplier
    6. SNR mapping to [0.0, 1.0] detection confidence.
    """
    health_state = env.sensor_health.get("Radar")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))
    
    if health_multiplier <= 0.0:
        return 0.0, {
            "sensor": "Radar",
            "base_score": 0.0,
            "effective_rcs_m2": 0.0,
            "snr_db": -99.0,
            "path_loss_factor": 0.0,
            "rf_attenuation_db": 0.0,
            "jamming_degradation": 0.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0
        }

    # 1. Target RCS modified by stealth rating
    effective_rcs = max(0.00005, rcs_m2 * (1.0 - stealth_rating * 0.92))

    # 2. Geometric Spreading Loss: Radar equation has R^4 dependence
    # Normalize baseline range at 10km for reference radar aperture
    dist_km = max(0.5, env.distance_km)
    range_factor = (10.0 / dist_km) ** 2.0  # Smooth R^-2 to R^-4 compressed mapping for stability

    # 3. Atmospheric Loss (dB and linear factor)
    rf_atten_rate = env.get_rf_attenuation_db_per_km()
    rf_atten_db = rf_atten_rate * dist_km
    atm_linear_loss = 10.0 ** (-rf_atten_db / 10.0)

    # 4. Electronic Jamming impact (reduces effective SNR)
    jamming_degradation = 1.0 / (1.0 + 15.0 * (env.jamming_level ** 1.5))

    # 5. Calculate Synthetic Signal Power & SNR (dB)
    raw_signal = (effective_rcs / 5.0) * range_factor * atm_linear_loss * jamming_degradation * health_multiplier
    snr_db = 10.0 * math.log10(max(1e-6, raw_signal)) + 15.0

    # 6. Map SNR (dB) to confidence score using Sigmoid curve centered at 0 dB SNR
    base_confidence = 1.0 / (1.0 + math.exp(-0.25 * snr_db))

    # 7. Apply stochastic measurement noise
    stochastic_noise_std = 0.03 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    metadata = {
        "sensor": "Radar",
        "base_score": round(base_confidence, 3),
        "effective_rcs_m2": round(effective_rcs, 5),
        "snr_db": round(snr_db, 2),
        "rf_attenuation_db": round(rf_atten_db, 2),
        "jamming_degradation": round(1.0 - jamming_degradation, 3),
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4)
    }

    return final_score, metadata
