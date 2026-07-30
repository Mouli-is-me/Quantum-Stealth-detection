"""
Explainability Engine Module
Generates human-readable, engineering-inspired justifications for every sensor reading.
"""

from typing import Dict, List, Any
from simulator.environment import EnvironmentConfig, Weather, SensorHealth


def generate_sensor_explanations(
    env: EnvironmentConfig,
    sensor_scores: Dict[str, float],
    sensor_metadata: Dict[str, Dict[str, Any]],
    target_info: Dict[str, Any]
) -> Dict[str, List[str]]:
    """
    Produces structured diagnostic explanations for each sensor modality.
    Returns: Dict[sensor_name, List[explanation_bullets]]
    """
    explanations: Dict[str, List[str]] = {}

    aircraft_type = target_info.get("aircraft_type", "Target")
    dist_km = env.distance_km
    weather = env.weather
    jamming = env.jamming_level
    stealth = target_info.get("stealth", 0.0)

    # --- RADAR EXPLANATION ---
    radar_score = sensor_scores.get("Radar", 0.0)
    radar_meta = sensor_metadata.get("Radar", {})
    radar_reasons = []

    if radar_score >= 0.70:
        radar_reasons.append(f"Strong radar echo returned for {aircraft_type} (effective RCS: {radar_meta.get('effective_rcs_m2', 'N/A')} m²).")
        if dist_km <= 30:
            radar_reasons.append(f"Short tracking distance ({dist_km:.1f} km) yields high signal-to-noise ratio.")
    else:
        if stealth > 0.6:
            radar_reasons.append(f"High stealth rating ({stealth:.2f}) significantly reduces radar cross-section (RCS: {radar_meta.get('effective_rcs_m2', 'N/A')} m²).")
        if dist_km > 40:
            radar_reasons.append(f"Extended range ({dist_km:.1f} km) induces R^-4 free-space path loss.")
        if weather in [Weather.RAIN, Weather.HEAVY_RAIN, Weather.SNOW]:
            radar_reasons.append(f"Atmospheric precipitation ({weather.value}) causes {radar_meta.get('rf_attenuation_db', 'N/A')} dB RF signal attenuation.")
        if jamming > 0.2:
            radar_reasons.append(f"Electronic jamming ({jamming * 100:.0f}% intensity) degrades radar SNR by {radar_meta.get('jamming_degradation', 0)*100:.1f}%.")

    if not radar_reasons:
        radar_reasons.append(f"Moderate radar return calculated for {aircraft_type} at distance {dist_km:.1f} km (SNR: {radar_meta.get('snr_db', 0):.1f} dB).")

    radar_health = env.sensor_health.get("Radar", SensorHealth.HEALTHY)
    if radar_health != SensorHealth.HEALTHY:
        radar_reasons.append(f"Radar hardware status is '{radar_health.value}' (confidence scaled by {radar_meta.get('health_multiplier', 1.0)}x).")

    explanations["Radar"] = radar_reasons

    # --- INFRARED EXPLANATION ---
    ir_score = sensor_scores.get("Infrared", 0.0)
    ir_meta = sensor_metadata.get("Infrared", {})
    ir_reasons = []

    if ir_score >= 0.70:
        ir_reasons.append(f"High thermal IR emission source ({ir_meta.get('ir_radiance_source', 'N/A')}) detected from target engine/exhaust.")
        if weather in [Weather.CLEAR, Weather.CLEAR_DAY]:
            ir_reasons.append("Clear atmospheric conditions allow high IR transmission.")
    else:
        if weather in [Weather.FOG, Weather.CLOUDY]:
            ir_reasons.append(f"Fog/clouds scatter IR wavelengths (atmospheric transmission down to {ir_meta.get('atm_transmission', 0)*100:.1f}%).")
        if dist_km > 35:
            ir_reasons.append(f"Distance of {dist_km:.1f} km attenuates infrared radiance intensity.")
        if target_info.get("engine_heat", 0.5) < 0.3:
            ir_reasons.append("Low engine heat emission output / masked exhaust plume.")

    if not ir_reasons:
        ir_reasons.append(f"Moderate IR detection score ({ir_score:.2f}) registered for target engine thermal plume at {dist_km:.1f} km.")

    ir_health = env.sensor_health.get("Infrared", SensorHealth.HEALTHY)
    if ir_health != SensorHealth.HEALTHY:
        ir_reasons.append(f"Infrared sensor status is '{ir_health.value}'.")

    explanations["Infrared"] = ir_reasons

    # --- THERMAL EXPLANATION ---
    thermal_score = sensor_scores.get("Thermal", 0.0)
    thermal_meta = sensor_metadata.get("Thermal", {})
    thermal_reasons = []

    mach = thermal_meta.get("mach_number", 0.0)
    skin_c = thermal_meta.get("skin_heating_c", 0.0)
    if mach > 0.9:
        thermal_reasons.append(f"High flight velocity (Mach {mach}) induces +{skin_c:.1f}°C aerodynamic skin friction heating.")
    if thermal_score >= 0.65:
        thermal_reasons.append(f"Apparent thermal signature delta is +{thermal_meta.get('total_thermal_signature_c', 0):.1f}°C above ambient background.")
    elif thermal_score < 0.35:
        thermal_reasons.append(f"Target thermal contrast attenuated by distance ({dist_km:.1f} km) and atmospheric absorption.")

    if not thermal_reasons:
        thermal_reasons.append(f"Thermal imaging registered +{thermal_meta.get('total_thermal_signature_c', 0):.1f}°C contrast above ambient environment.")

    explanations["Thermal"] = thermal_reasons

    # --- ACOUSTIC EXPLANATION ---
    acoustic_score = sensor_scores.get("Acoustic", 0.0)
    acoustic_meta = sensor_metadata.get("Acoustic", {})
    acoustic_reasons = []

    received_spl = acoustic_meta.get("received_spl_db", 0.0)
    ambient_noise = acoustic_meta.get("ambient_noise_floor_db", 0.0)

    if acoustic_score >= 0.60:
        acoustic_reasons.append(f"Target acoustic signature ({acoustic_meta.get('source_spl_db', 0):.1f} dB SPL) exceeds ambient noise floor ({ambient_noise:.1f} dB SPL).")
        if "Helicopter" in aircraft_type:
            acoustic_reasons.append("Distinctive low-frequency main rotor blade slap detected.")
    else:
        if dist_km > 15:
            acoustic_reasons.append(f"Long propagation distance ({dist_km:.1f} km) causes acoustic spherical spreading and absorption loss.")
        if weather in [Weather.RAIN, Weather.HEAVY_RAIN]:
            acoustic_reasons.append(f"Rainfall elevates acoustic background noise floor to {ambient_noise:.1f} dB SPL.")
        if "Bird" in aircraft_type or "Drone" in aircraft_type:
            acoustic_reasons.append(f"{aircraft_type} generates low intrinsic sound pressure level.")

    if not acoustic_reasons:
        acoustic_reasons.append(f"Acoustic sensor array registered signal-to-noise ratio of {acoustic_meta.get('snr_acoustic_db', 0):.1f} dB.")

    explanations["Acoustic"] = acoustic_reasons

    # --- EO CAMERA EXPLANATION ---
    eo_score = sensor_scores.get("EO_Camera", 0.0)
    eo_meta = sensor_metadata.get("EO_Camera", {})
    eo_reasons = []

    if eo_score >= 0.70:
        eo_reasons.append(f"Clear visual optical contrast ({eo_meta.get('apparent_contrast', 0):.3f}) under good visibility ({eo_meta.get('visibility_km', 0)} km).")
    else:
        if weather == Weather.NIGHT:
            eo_reasons.append("Low nighttime solar illuminance reduces daylight camera optical contrast.")
        if weather in [Weather.FOG, Weather.RAIN, Weather.HEAVY_RAIN]:
            eo_reasons.append(f"Precipitation/fog ({weather.value}) restricts visual range (extinction coef sigma={eo_meta.get('extinction_coef_sigma', 0):.3f}).")
        if dist_km > 20:
            eo_reasons.append(f"Distance of {dist_km:.1f} km degrades camera angular resolution.")

    if not eo_reasons:
        eo_reasons.append(f"Electro-Optical camera operating under {weather.value} visibility conditions.")

    explanations["EO_Camera"] = eo_reasons

    return explanations
