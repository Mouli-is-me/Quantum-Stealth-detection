from typing import Dict, List

def calculate_fusion_weights(scores: Dict[str, float], selected_sensors: List[str]) -> Dict[str, float]:
    """
    Calculate normalized fusion weights for each sensor.
    Selected sensors get weights proportional to their confidence, uncertainty, and agreement.
    Excluded sensors receive a weight of 0.0.
    
    Args:
        scores: Dictionary of sensor confidence scores.
        selected_sensors: List of selected sensor names.
        
    Returns:
        Dictionary mapping sensor names to normalized weights summing to 1.
    """
    # Initialize all weights to 0.0
    weights = {sensor: 0.0 for sensor in scores.keys()}
    
    if not selected_sensors:
        # Fallback if no sensors are selected: distribute weights equally
        n = len(scores)
        if n > 0:
            for s in scores.keys():
                weights[s] = round(1.0 / n, 3)
        return weights

    # Calculate raw weights for selected sensors
    raw_weights = {}
    for i in selected_sensors:
        c_i = scores[i]
        # Uncertainty
        u_i = 1.0 - c_i
        
        # Agreement factor with other selected sensors
        if len(selected_sensors) > 1:
            total_disagreement = sum(abs(c_i - scores[j]) for j in selected_sensors if j != i)
            avg_disagreement = total_disagreement / (len(selected_sensors) - 1)
            agreement = 1.0 - avg_disagreement
        else:
            agreement = 1.0
            
        # Raw weight incorporates confidence, uncertainty, and agreement
        # Using max(0, ...) to ensure positive raw weights
        raw_w = max(0.0, c_i * (1.0 - u_i) * agreement)
        raw_weights[i] = raw_w

    total_raw_weight = sum(raw_weights.values())
    if total_raw_weight == 0.0:
        # Fallback if all raw weights are zero: equal weight among selected
        for i in selected_sensors:
            weights[i] = round(1.0 / len(selected_sensors), 3)
    else:
        # Normalize and round weights
        for i in selected_sensors:
            weights[i] = round(raw_weights[i] / total_raw_weight, 3)
            
    # Normalize to ensure they sum to exactly 1.0 (handling float rounding)
    total_normalized = sum(weights.values())
    if selected_sensors and total_normalized != 1.0:
        # Adjust the first selected sensor by the tiny difference
        diff = 1.0 - total_normalized
        weights[selected_sensors[0]] = round(weights[selected_sensors[0]] + diff, 3)
        
    return weights
