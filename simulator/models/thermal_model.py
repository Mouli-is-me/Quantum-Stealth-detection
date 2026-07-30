"""
Thermal Sensor Model
Computes Thermal sensor confidence based on aerodynamic skin friction heating, engine thermal flux,
ambient contrast, and atmospheric extinction.
"""

import math
from typing import Dict, Any, Tuple
from simulator.profiles import AircraftProfile
from simulator.environment import EnvironmentConfig, HEALTH_MULTIPLIERS
from simulator.noise import NoiseEngine


def calculate_thermal_confidence(
    profile: AircraftProfile,
    env: EnvironmentConfig,
    speed_knots: float,
    thermal_delta_c: float,
    engine_heat: float,
    noise_engine: NoiseEngine
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates Thermal imaging sensor detection confidence [0.0, 1.0].
    
    Physics Model:
    1. Aerodynamic Heating: T_skin_delta = T_ambient * 0.2 * (Mach^2)
    2. Engine Thermal Flux = thermal_delta_c * (0.5 + 0.5 * engine_heat)
    3. Total Thermal Delta = T_skin_delta + Engine Thermal Flux
    4. Atmospheric Transmission loss over distance
    5. Sensor Health Multiplier
    """
    health_state = env.sensor_health.get("Thermal")
    health_multiplier, noise_multiplier = HEALTH_MULTIPLIERS.get(health_state, (1.0, 1.0))

    if health_multiplier <= 0.0:
        return 0.0, {
            "sensor": "Thermal",
            "base_score": 0.0,
            "mach_number": 0.0,
            "skin_heating_c": 0.0,
            "engine_thermal_delta_c": 0.0,
            "total_thermal_signature_c": 0.0,
            "health_multiplier": 0.0,
            "noise_added": 0.0
        }

    dist_km = max(0.5, env.distance_km)

    # 1. Mach number & Aerodynamic skin heating
    speed_mps = speed_knots * 0.514444
    sound_speed_mps = 340.0
    mach = speed_mps / sound_speed_mps
    ambient_k = env.ambient_temp_c + 273.15
    skin_heating_c = ambient_k * 0.2 * (mach ** 2.0)

    # 2. Engine Thermal output
    engine_thermal_c = thermal_delta_c * (0.4 + 0.6 * engine_heat)

    # 3. Combined Apparent Thermal Signature (°C above ambient)
    total_thermal_sig_c = skin_heating_c + engine_thermal_c

    # 4. Atmospheric Extinction & Range attenuation
    gamma_thermal = env.get_ir_extinction_coef() * 0.9  # LWIR band transmission
    range_decay = (20.0 / dist_km) ** 1.1
    atm_trans = math.exp(-gamma_thermal * dist_km)

    apparent_thermal_signal = (total_thermal_sig_c / 40.0) * range_decay * atm_trans * health_multiplier

    # Map to [0.0, 1.0]
    base_confidence = min(1.0, max(0.0, 1.0 - math.exp(-0.85 * apparent_thermal_signal)))

    # 5. Apply noise
    stochastic_noise_std = 0.03 * noise_multiplier
    noisy_confidence, noise_added = noise_engine.apply_noise(
        base_confidence,
        noise_level=stochastic_noise_std,
        distribution="gaussian"
    )

    final_score = round(noisy_confidence, 2)

    metadata = {
        "sensor": "Thermal",
        "base_score": round(base_confidence, 3),
        "mach_number": round(mach, 2),
        "skin_heating_c": round(skin_heating_c, 2),
        "engine_thermal_delta_c": round(engine_thermal_c, 2),
        "total_thermal_signature_c": round(total_thermal_sig_c, 2),
        "health_multiplier": health_multiplier,
        "noise_added": round(noise_added, 4)
    }

    return final_score, metadata
