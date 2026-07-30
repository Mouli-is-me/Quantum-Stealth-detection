"""
Acoustic Sensor Model
Computes Acoustic detection confidence using spherical sound propagation, atmospheric absorption loss,
engine/rotor sound pressure level (SPL), and background ambient noise floor.
"""

import math
from typing import Dict, Any, Tuple
from simulator.profiles import AircraftProfile
from simulator.environment import EnvironmentConfig, Weather, HEALTH_MULTIPLIERS
from simulator.noise import NoiseEngine


def calculate_acoustic_confidence(
    profile: AircraftProfile,
    env: EnvironmentConfig,
    acoustic_spl_db: float,
    noise_factor: float,
    noise_engine: NoiseEngine
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates Acoustic detection confidence [0.0, 1.0].
    
    Physics Model:
    1. Source SPL at 1m (dB SPL) = acoustic_spl_db * (0.8 + 0.4 * noise_factor)
    2. Spherical Spreading Loss = 20 * log10(distance_meters)
    3. Atmospheric Absorption = alpha_ac_db_per_km * distance_km
    4. Received SPL = Source_SPL - Spreading_Loss - Absorption
    5. Ambient Noise Floor (wind, rain, weather)
    6. Acoustic SNR (dB) = Received_SPL - Ambient_Noise_Floor
    7. Sensor Health & Noise
    """
    health_state = env.sensor_health.get("Acoustic")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))

    if health_multiplier <= 0.0:
        return 0.0, {
            "sensor": "Acoustic",
            "base_score": 0.0,
            "source_spl_db": 0.0,
            "received_spl_db": 0.0,
            "ambient_noise_floor_db": 0.0,
            "snr_acoustic_db": -99.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0
        }

    dist_km = max(0.1, env.distance_km)
    dist_m = dist_km * 1000.0

    # 1. Source Sound Pressure Level (dB SPL at 1 meter)
    source_spl = acoustic_spl_db * (0.85 + 0.3 * noise_factor)

    # 2. Geometric Inverse-Square Spherical Spreading Loss (dB)
    spherical_loss_db = 20.0 * math.log10(max(1.0, dist_m))

    # 3. Atmospheric Absorption (dB)
    alpha_ac = env.get_acoustic_absorption_db_per_km()
    abs_loss_db = alpha_ac * dist_km

    # 4. Received Sound Pressure Level at Sensor Array
    received_spl = source_spl - spherical_loss_db - abs_loss_db

    # 5. Background Ambient Noise Floor (wind/rain acoustic interference)
    base_ambient_db = 45.0  # Quiet rural/airfield baseline
    if env.weather == Weather.RAIN:
        base_ambient_db += 18.0  # Rain impact noise
    elif env.weather == Weather.SNOW:
        base_ambient_db += 8.0
    elif env.weather == Weather.FOG:
        base_ambient_db -= 5.0   # Fog dampens high frequency ambient

    ambient_noise_floor = base_ambient_db + noise_factor * 15.0

    # 6. Acoustic Signal-to-Noise Ratio (dB)
    snr_acoustic_db = received_spl - ambient_noise_floor

    # 7. Map Acoustic SNR to detection confidence using Sigmoid
    base_confidence = 1.0 / (1.0 + math.exp(-0.2 * (snr_acoustic_db - 3.0))) * health_multiplier
    base_confidence = min(1.0, max(0.0, base_confidence))

    # 8. Apply measurement noise
    stochastic_noise_std = 0.04 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    metadata = {
        "sensor": "Acoustic",
        "base_score": round(base_confidence, 3),
        "source_spl_db": round(source_spl, 1),
        "received_spl_db": round(received_spl, 1),
        "ambient_noise_floor_db": round(ambient_noise_floor, 1),
        "snr_acoustic_db": round(snr_acoustic_db, 1),
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4)
    }

    return final_score, metadata
