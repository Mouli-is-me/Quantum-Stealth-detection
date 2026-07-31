from typing import Dict, Any, List

def classical_sensor_fusion(scores: Dict[str, float], threshold: float = 0.45) -> Dict[str, Any]:
    """
    Classical weighted sensor fusion baseline.
    Supports legacy sensors with original weights, generalizes to any number of sensors,
    and returns a structured output consistent with the quantum optimizer.
    
    Args:
        scores: Dictionary of sensor confidence scores.
        threshold: Detection threshold. Default 0.45.
        
    Returns:
        Dict[str, Any]: Structured baseline results.
    """
    # 1. Determine weights
    legacy_keys = {"Radar", "Infrared", "Acoustic"}
    if set(scores.keys()) == legacy_keys:
        weights = {
            "Radar": 0.40,
            "Infrared": 0.30,
            "Acoustic": 0.30
        }
    else:
        # Distribute weights equally for generalized sensor suites
        n = len(scores)
        if n > 0:
            equal_w = round(1.0 / n, 3)
            weights = {s: equal_w for s in scores.keys()}
            # Adjust rounding errors to sum to exactly 1.0
            total_w = sum(weights.values())
            if total_w != 1.0:
                first_key = list(scores.keys())[0]
                weights[first_key] = round(weights[first_key] + (1.0 - total_w), 3)
        else:
            weights = {}

    # 2. Compute metrics
    # Weighted confidence (fusion score)
    weighted_confidence = sum(scores[s] * weights.get(s, 0.0) for s in scores.keys())
    
    # Average confidence across all sensors
    average_confidence = sum(scores.values()) / len(scores) if scores else 0.0
    
    # Selected sensors (those meeting or exceeding the detection threshold)
    selected_sensors = [s for s, score in scores.items() if score >= threshold]
    
    # Fallback to highest confidence if none meet threshold
    if not selected_sensors and scores:
        best_sensor = max(scores, key=scores.get)
        selected_sensors = [best_sensor]
        
    detected = weighted_confidence >= threshold
    
    # 3. Calculate comparison and variation metrics
    max_score = max(scores.values()) if scores else 0.0
    min_score = min(scores.values()) if scores else 0.0
    variance = sum((scores[s] - average_confidence) ** 2 for s in scores.keys()) / len(scores) if scores else 0.0
    
    comparison_metrics = {
        "max_score": round(max_score, 3),
        "min_score": round(min_score, 3),
        "score_spread": round(max_score - min_score, 3),
        "score_variance": round(variance, 3),
        "threshold_met": [s for s, score in scores.items() if score >= threshold]
    }
    
    # 4. Generate dynamic explanation for the classical method
    selected_str = ", ".join(selected_sensors)
    reason = (
        f"Classical method fused {len(scores)} sensors using pre-defined weights. "
        f"Selected {selected_str} based on a threshold of {threshold}. "
        f"Overall weighted confidence is {weighted_confidence:.2f}."
    )
    
    return {
        # Legacy fields for backward compatibility
        "fusion_score": round(weighted_confidence, 3),
        "detected": detected,
        "method": "Classical Weighted Fusion",
        
        # Extended fields for consistent API
        "average_confidence": round(average_confidence, 3),
        "weighted_confidence": round(weighted_confidence, 3),
        "selected_sensors": selected_sensors,
        "selection": {s: (s in selected_sensors) for s in scores.keys()},
        "selected_count": len(selected_sensors),
        "weights": weights,
        "comparison_metrics": comparison_metrics,
        "reason": reason
    }
