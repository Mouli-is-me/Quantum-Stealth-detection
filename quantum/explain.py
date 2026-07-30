from typing import Dict, List

def generate_explanation(scores: Dict[str, float], selected_sensors: List[str], weights: Dict[str, float]) -> str:
    """
    Dynamically generates a human-readable explanation of why sensors were selected
    and how their weights were distributed, avoiding hardcoded names.
    
    Args:
        scores: Dictionary mapping sensor names to their confidence scores.
        selected_sensors: List of selected sensor names.
        weights: Dictionary mapping sensor names to their normalized weights.
        
    Returns:
        A human-readable explanation string.
    """
    if not selected_sensors:
        return "No sensors were selected because their individual confidences were too low or they were highly conflicting."
    
    active_explanations = []
    inactive_explanations = []
    
    # Sort selected sensors by weight descending
    sorted_selected = sorted(selected_sensors, key=lambda s: weights.get(s, 0.0), reverse=True)
    
    # High weight sensors (above average weight among selected)
    avg_weight = 1.0 / len(selected_sensors)
    high_weight_sensors = [s for s in sorted_selected if weights.get(s, 0.0) >= avg_weight]
    low_weight_selected = [s for s in sorted_selected if weights.get(s, 0.0) < avg_weight]
    
    if high_weight_sensors:
        names = " and ".join(high_weight_sensors) if len(high_weight_sensors) > 1 else high_weight_sensors[0]
        verb = "were" if len(high_weight_sensors) > 1 else "was"
        active_explanations.append(
            f"{names} {verb} assigned higher weights because they had higher confidence and lower uncertainty."
        )
        
    if low_weight_selected:
        names = " and ".join(low_weight_selected) if len(low_weight_selected) > 1 else low_weight_selected[0]
        verb = "contributed" if len(low_weight_selected) > 1 else "contributed"
        active_explanations.append(
            f"{names} {verb} less due to larger uncertainty or lower relative confidence."
        )
        
    # Inactive sensors
    inactive_sensors = [s for s in scores.keys() if s not in selected_sensors]
    if inactive_sensors:
        names = " and ".join(inactive_sensors) if len(inactive_sensors) > 1 else inactive_sensors[0]
        verb = "were" if len(inactive_sensors) > 1 else "was"
        inactive_explanations.append(
            f"{names} {verb} excluded because of high uncertainty or significant disagreement with the selected sensors."
        )
        
    explanation_parts = active_explanations + inactive_explanations
    return " ".join(explanation_parts)
