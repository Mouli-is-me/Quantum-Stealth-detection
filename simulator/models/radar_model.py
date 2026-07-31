"""
Radar Sensor Model
Computes radar detection confidence using the Radar Range Equation, RCS, atmospheric attenuation,
stealth factors, electronic jamming, sensor health, and actual operational detection distance.
"""

import math
from typing import Dict, Any, Tuple, Optional
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
    Calculates Radar detection confidence [0.0, 1.0] and actual scenario detection distance.
    """
    health_state = env.sensor_health.get("Radar")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))
    
    if health_multiplier <= 0.0:
        metadata = {
            "sensor": "Radar",
            "base_score": 0.0,
            "effective_rcs_m2": 0.0,
            "snr_db": -99.0,
            "rf_attenuation_db": 0.0,
            "jamming_degradation": 0.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0,
            "detection_distance_km": None,
            "status": "Not Detected",
            "reason": "Sensor offline or unserviceable"
        }
        return 0.0, metadata

    # 1. Target RCS modified by stealth rating
    effective_rcs = max(0.00005, rcs_m2 * (1.0 - stealth_rating * 0.92))

    # 2. Geometric Spreading Loss
    dist_km = max(0.5, env.distance_km)
    range_factor = (10.0 / dist_km) ** 2.0

    # 3. Atmospheric Loss
    rf_atten_rate = env.get_rf_attenuation_db_per_km()
    rf_atten_db = rf_atten_rate * dist_km
    atm_linear_loss = 10.0 ** (-rf_atten_db / 10.0)

    # 4. Electronic Jamming impact
    jamming_degradation = 1.0 / (1.0 + 15.0 * (env.jamming_level ** 1.5))

    # 5. Calculate Synthetic Signal Power & SNR (dB)
    raw_signal = (effective_rcs / 5.0) * range_factor * atm_linear_loss * jamming_degradation * health_multiplier
    snr_db = 10.0 * math.log10(max(1e-6, raw_signal)) + 15.0

    # 6. Map SNR (dB) to confidence score
    base_confidence = 1.0 / (1.0 + math.exp(-0.25 * snr_db))

    # 7. Apply stochastic measurement noise
    stochastic_noise_std = 0.03 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    # 8. Calculate Actual Operational Detection Distance
    det_dist_km, status, reason = _calculate_radar_detection_distance(
        effective_rcs=effective_rcs,
        rf_atten_rate=rf_atten_rate,
        jamming_level=env.jamming_level,
        health_multiplier=health_multiplier,
        final_score=final_score
    )

    metadata = {
        "sensor": "Radar",
        "base_score": round(base_confidence, 3),
        "effective_rcs_m2": round(effective_rcs, 5),
        "snr_db": round(snr_db, 2),
        "rf_attenuation_db": round(rf_atten_db, 2),
        "jamming_degradation": round(1.0 - jamming_degradation, 3),
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4),
        "detection_distance_km": det_dist_km,
        "status": status,
        "reason": reason
    }

    return final_score, metadata


def _calculate_radar_detection_distance(
    effective_rcs: float,
    rf_atten_rate: float,
    jamming_level: float,
    health_multiplier: float,
    final_score: float
) -> Tuple[Optional[float], str, str]:
    """Calculates operational radar detection range under current physics conditions."""
    if health_multiplier <= 0.0 or final_score < 0.15:
        return None, "Not Detected", "Signal below radar detection threshold"

    # Physics range scaling: R ~ (RCS^0.25) adjusted for jamming & RF loss
    base_range = 42.0 * (effective_rcs ** 0.28) * (1.0 / (1.0 + 6.0 * (jamming_level ** 1.3))) * (health_multiplier ** 0.5)
    attenuation_factor = 1.0 + (rf_atten_rate * 0.7)
    det_dist = max(1.2, base_range / attenuation_factor)
    det_dist = round(det_dist, 1)

    reasons = []
    if rf_atten_rate > 0.4:
        reasons.append("heavy rain")
    elif rf_atten_rate > 0.15:
        reasons.append("atmospheric moisture")
    if effective_rcs < 0.005:
        reasons.append("stealth coating")
    elif effective_rcs < 0.1:
        reasons.append("low RCS profile")
    if jamming_level > 0.3:
        reasons.append("electronic jamming")

    if reasons:
        reason_str = f"Reduced by {', '.join(reasons)}"
    else:
        reason_str = "Optimal radar return signal"

    return det_dist, "Detected", reason_str
