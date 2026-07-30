"""
Adaptive Multi-Sensor Fusion Engine
Combines multi-modal sensor inputs dynamically based on physics, health, noise, and consensus.
"""

from typing import Dict, Any, List, Tuple
from fusion.config import (
    BASE_RELIABILITIES, WEATHER_MODIFIERS, HEALTH_PENALTIES,
    DISTANCE_OPTIMAL, DISTANCE_LIMIT, DISAGREEMENT_THRESHOLD
)


def adaptive_sensor_fusion(
    sensor_scores: Dict[str, float],
    env_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Executes the confidence-weighted, explainable adaptive sensor fusion pipeline.
    
    Inputs:
      - sensor_scores: Dict[sensor_name, score_float] (e.g. {'Radar': 0.85, 'Infrared': 0.62, ...})
      - env_data: Dict containing environment settings, distance, weather, health, etc.
      
    Outputs a rich dictionary of fusion metrics and diagnostic explanations.
    """
    # 1. Input Validation & Default Sanitization
    active_sensors = ["Radar", "Infrared", "Thermal", "Acoustic", "EO_Camera"]
    validated_scores: Dict[str, float] = {}
    for s in active_sensors:
        val = sensor_scores.get(s, env_data.get(s, 0.0))
        validated_scores[s] = max(0.0, min(1.0, float(val)))

    weather = env_data.get("weather_detailed", env_data.get("weather", "Clear"))
    dist_km = float(env_data.get("distance", 25.0))
    jamming = float(env_data.get("jamming", 0.0))

    health_raw = env_data.get("sensor_health", {})
    health_dict: Dict[str, str] = {}
    for s in active_sensors:
        health_dict[s] = str(health_raw.get(s, "Healthy"))

    # Extract noise contributions from simulator metadata if present
    meta_raw = env_data.get("metadata", {})
    noise_dict: Dict[str, float] = {}
    for s in active_sensors:
        s_meta = meta_raw.get(s, {})
        noise_dict[s] = abs(float(s_meta.get("noise_added", 0.02)))

    # 2. Reliability & Environmental Assessment
    sensor_reliabilities: Dict[str, float] = {}
    weather_adj: Dict[str, float] = {}
    
    weath_row = WEATHER_MODIFIERS.get(weather, WEATHER_MODIFIERS["Clear"])

    for s in active_sensors:
        base_r = BASE_RELIABILITIES[s]
        health_state = health_dict[s]
        health_mult = HEALTH_PENALTIES.get(health_state, 1.0)
        weath_mult = weath_row.get(s, 1.0)

        # Distance degradation scaling
        dist_factor = 1.0
        if dist_km > DISTANCE_OPTIMAL:
            decay_rate = 0.012 if s in ["Radar", "Acoustic"] else 0.008
            dist_factor = max(0.15, 1.0 - (dist_km - DISTANCE_OPTIMAL) * decay_rate)

        calculated_r = base_r * health_mult * weath_mult * dist_factor
        sensor_reliabilities[s] = calculated_r
        weather_adj[s] = weath_mult

    # 3. Dynamic Weight Calculation
    raw_weights: Dict[str, float] = {}
    total_raw_weight = 0.0

    for s in active_sensors:
        if health_dict[s] == "Offline":
            raw_weights[s] = 0.0
            continue

        noise_penalty = max(0.5, 1.0 - noise_dict[s] * 1.5)
        raw_w = sensor_reliabilities[s] * noise_penalty
        raw_weights[s] = raw_w
        total_raw_weight += raw_w

    # Normalize weights
    normalized_weights: Dict[str, float] = {}
    if total_raw_weight > 0.0:
        for s in active_sensors:
            normalized_weights[s] = round(raw_weights[s] / total_raw_weight, 3)
    else:
        active_count = sum(1 for s in active_sensors if health_dict[s] != "Offline")
        for s in active_sensors:
            if health_dict[s] != "Offline":
                normalized_weights[s] = round(1.0 / max(1, active_count), 3)
            else:
                normalized_weights[s] = 0.0

    # Sensor Contribution Percentages
    sensor_contributions: Dict[str, str] = {
        s: f"{normalized_weights[s] * 100.0:.1f}%" for s in active_sensors
    }

    # 4. Confidence-Weighted Fusion
    fusion_score = 0.0
    for s in active_sensors:
        fusion_score += validated_scores[s] * normalized_weights[s]

    # 5. Sensor Disagreement Analysis
    disagreements: List[str] = []
    max_delta = 0.0
    active_scores_list = []
    
    for s in active_sensors:
        if health_dict[s] == "Offline":
            continue
        delta = abs(validated_scores[s] - fusion_score)
        active_scores_list.append(validated_scores[s])
        if delta > max_delta:
            max_delta = delta
        if delta > DISAGREEMENT_THRESHOLD:
            disagreements.append(s)

    import numpy as np
    if len(active_scores_list) > 1:
        base_std = float(np.std(active_scores_list))
    else:
        base_std = 0.0

    disagreement_penalty = 0.15 * len(disagreements)
    uncertainty = min(1.0, max(0.0, base_std + disagreement_penalty))

    # 6. Overall Reliability Score & Confidence Estimation
    active_reliabilities = [sensor_reliabilities[s] for s in active_sensors if health_dict[s] != "Offline"]
    avg_reliability = sum(active_reliabilities) / len(active_reliabilities) if active_reliabilities else 0.0

    overall_confidence = fusion_score * (1.0 - 0.35 * uncertainty) * max(0.1, avg_reliability)
    overall_confidence = round(max(0.0, min(1.0, overall_confidence)), 2)

    threat_confidence = round(fusion_score, 2)
    sensor_rankings = sorted(active_sensors, key=lambda x: normalized_weights[x], reverse=True)
    recommended_sensors = [s for s in sensor_rankings if normalized_weights[s] >= 0.15 and health_dict[s] != "Offline"]

    # 7. Explanation Generation
    explanation_bullets = []
    explanation_bullets.append(f"Operational Environment is '{weather}' at target range {dist_km:.1f} km.")

    degraded_list = [s for s in active_sensors if normalized_weights[s] < 0.10 and health_dict[s] != "Offline"]
    strongest_sensor = sensor_rankings[0]

    if degraded_list:
        explanation_bullets.append(f"Weights for {', '.join(degraded_list)} were reduced due to environmental constraints or high noise.")
    explanation_bullets.append(f"Primary fusion contribution assigned to {strongest_sensor} (weight: {normalized_weights[strongest_sensor]*100:.1f}%).")

    failed_list = [s for s in active_sensors if health_dict[s] in ["Offline", "Faulty", "Jammed"]]
    if failed_list:
        explanation_bullets.append(f"Critical health degradation detected on {', '.join(failed_list)}.")

    if disagreements:
        explanation_bullets.append(f"Observational conflict detected on {', '.join(disagreements)} (disagreement delta: {max_delta:.2f}); uncertainty increased to {uncertainty*100:.1f}%.")
    else:
        explanation_bullets.append("Consistent sensor agreement observed; sensor observations align with weighted consensus.")

    explanation_str = " ".join(explanation_bullets)

    # Individual Sensor Explanations Dictionary
    sensor_explanations: Dict[str, str] = {}
    for s in active_sensors:
        if health_dict[s] == "Offline":
            sensor_explanations[s] = "Sensor is Offline and excluded from fusion calculations."
        else:
            sensor_explanations[s] = (
                f"Weight: {sensor_contributions[s]}, Health: {health_dict[s]}, "
                f"Weather Modifier: {weather_adj[s]}x, Calculated Reliability: {sensor_reliabilities[s]:.2f}."
            )

    # 8. Return formatted dict (100% backward compatible structure)
    return {
        "fusion_score": round(fusion_score, 2),
        "overall_confidence": overall_confidence,
        "reliability_score": round(avg_reliability, 2),
        "uncertainty": round(uncertainty, 2),
        "threat_confidence": threat_confidence,
        "sensor_weights": normalized_weights,
        "sensor_contributions": sensor_contributions,
        "sensor_rankings": sensor_rankings,
        "recommended_sensors": recommended_sensors,
        "sensor_health_summary": health_dict,
        "disagreement_analysis": {
            "disagreements_found": len(disagreements) > 0,
            "disagreeing_sensors": disagreements,
            "max_delta": round(max_delta, 3),
            "uncertainty_penalty": round(disagreement_penalty, 3)
        },
        "environmental_adjustments": weather_adj,
        "explanation": explanation_str,
        "sensor_explanations": sensor_explanations,
        "fusion_metadata": {
            "distance_km": dist_km,
            "weather": weather,
            "jamming_level": jamming,
            "active_sensor_count": len(active_scores_list)
        }
    }
