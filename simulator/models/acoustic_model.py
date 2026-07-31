"""
Acoustic Sensor Model
Computes Acoustic detection confidence using spherical sound propagation, atmospheric absorption loss,
engine/rotor sound pressure level (SPL), background ambient noise floor, and actual scenario detection distance.
"""

import math
from typing import Dict, Any, Tuple, Optional
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
    Calculates Acoustic detection confidence [0.0, 1.0] and operational detection distance.
    """
    health_state = env.sensor_health.get("Acoustic")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))

    if health_multiplier <= 0.0:
        metadata = {
            "sensor": "Acoustic",
            "base_score": 0.0,
            "source_spl_db": 0.0,
            "received_spl_db": 0.0,
            "ambient_noise_floor_db": 0.0,
            "snr_acoustic_db": -99.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0,
            "detection_distance_km": None,
            "status": "Not Detected",
            "reason": "Sensor offline or unserviceable"
        }
        return 0.0, metadata

    dist_km = max(0.1, env.distance_km)
    dist_m = dist_km * 1000.0

    # 1. Source Sound Pressure Level (dB SPL at 1 meter)
    source_spl = acoustic_spl_db * (0.85 + 0.3 * noise_factor)

    # 2. Geometric Spherical Spreading Loss (dB)
    spherical_loss_db = 20.0 * math.log10(max(1.0, dist_m))

    # 3. Atmospheric Absorption (dB)
    alpha_ac = env.get_acoustic_absorption_db_per_km()
    abs_loss_db = alpha_ac * dist_km

    # 4. Received Sound Pressure Level
    received_spl = source_spl - spherical_loss_db - abs_loss_db

    # 5. Background Ambient Noise Floor
    base_ambient_db = 45.0
    if env.weather in [Weather.DRIZZLE, Weather.LIGHT_RAIN, Weather.RAIN]:
        base_ambient_db += 18.0
    elif env.weather in [Weather.HEAVY_RAIN, Weather.THUNDERSTORM]:
        base_ambient_db += 28.0
    elif env.weather in [Weather.CROSS_WIND, Weather.STRONG_WIND]:
        base_ambient_db += 22.0
    elif env.weather in [Weather.SNOW, Weather.HEAVY_SNOW]:
        base_ambient_db += 8.0
    elif env.weather in [Weather.MORNING_FOG, Weather.FOG, Weather.DENSE_FOG]:
        base_ambient_db -= 5.0

    ambient_noise_floor = base_ambient_db + noise_factor * 15.0

    # 6. Acoustic Signal-to-Noise Ratio (dB)
    snr_acoustic_db = received_spl - ambient_noise_floor

    # 7. Map Acoustic SNR to confidence score
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

    # 9. Calculate Actual Operational Detection Distance
    det_dist_km, status, reason = _calculate_acoustic_detection_distance(
        source_spl=source_spl,
        ambient_noise_floor=ambient_noise_floor,
        alpha_ac=alpha_ac,
        env=env,
        health_multiplier=health_multiplier,
        final_score=final_score
    )

    metadata = {
        "sensor": "Acoustic",
        "base_score": round(base_confidence, 3),
        "source_spl_db": round(source_spl, 1),
        "received_spl_db": round(received_spl, 1),
        "ambient_noise_floor_db": round(ambient_noise_floor, 1),
        "snr_acoustic_db": round(snr_acoustic_db, 1),
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4),
        "detection_distance_km": det_dist_km,
        "status": status,
        "reason": reason
    }

    return final_score, metadata


def _calculate_acoustic_detection_distance(
    source_spl: float,
    ambient_noise_floor: float,
    alpha_ac: float,
    env: EnvironmentConfig,
    health_multiplier: float,
    final_score: float
) -> Tuple[Optional[float], str, str]:
    """Calculates operational acoustic detection range based on sound propagation and ambient noise floor."""
    if health_multiplier <= 0.0 or final_score < 0.20 or source_spl <= ambient_noise_floor:
        if source_spl < 60.0:
            reason_str = "Ultra-low acoustic signature below ambient noise floor"
        elif ambient_noise_floor > 65.0:
            reason_str = "Masked by heavy rain and wind noise interference"
        else:
            reason_str = "Acoustic attenuation over range"
        return None, "Not Detected", reason_str

    # Maximum allowable path loss in dB before signal equals ambient floor
    max_loss_db = max(0.0, source_spl - ambient_noise_floor)
    
    # Spherical spreading model range: 20*log10(1000*R) + alpha*R = max_loss
    # Approximate solver for R_km
    approx_range_km = (10.0 ** ((max_loss_db - 60.0) / 20.0)) / (1.0 + (alpha_ac * 0.05))
    det_dist = round(max(0.3, min(approx_range_km, 35.0)), 1)

    reasons = []
    if ambient_noise_floor > 60.0:
        reasons.append("high background wind/rain noise")
    if source_spl < 80.0:
        reasons.append("quiet electric/rotor motor signature")
    if alpha_ac > 7.0:
        reasons.append("atmospheric acoustic absorption")

    if reasons:
        reason_str = f"Constrained by {', '.join(reasons)}"
    else:
        reason_str = "High acoustic sound pressure level return"

    return det_dist, "Detected", reason_str
