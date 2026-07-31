"""
Explainable AI Prediction Module
Provides backward-compatible predict(sensor_data) and comprehensive predict_explainable(...) functions.
"""

import joblib
import pandas as pd
from typing import Dict, Any, Tuple, Optional

from ai.xai_engine import XAIEngine

# Load underlying ML model if available
try:
    model = joblib.load("ai/model.pkl")
except Exception:
    model = None


def predict(sensor_data: Dict[str, Any]) -> Tuple[int, float]:
    """
    100% Backward Compatible Prediction API.
    Returns: (prediction: int (0 or 1), confidence: float [0.0, 1.0])
    """
    res = predict_explainable(sensor_data)
    return res["prediction"], res["confidence"]


def predict_explainable(
    sensor_data: Dict[str, Any],
    fusion_result: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Comprehensive Explainable AI (XAI) Prediction API.
    
    Returns structured XAI diagnostic dictionary containing:
      - prediction (0 or 1)
      - predicted_class (str)
      - prediction_probability (float)
      - confidence (float)
      - threat_level ('Low', 'Medium', 'High', 'Critical')
      - feature_importance (Dict[str, float])
      - top_contributing_sensors (List[str])
      - reasoning (str)
      - uncertainty (float)
      - recommendation (str)
      - ai_metadata (Dict)
    """
    # 1. Target Class Prediction
    predicted_class, proba = XAIEngine.classify_target_type(sensor_data)

    # 2. Extract Sensor Scores
    sensor_scores = {
        "Radar": float(sensor_data.get("Radar", sensor_data.get("radar", 0.0))),
        "Infrared": float(sensor_data.get("Infrared", sensor_data.get("infrared", 0.0))),
        "Thermal": float(sensor_data.get("Thermal", 0.0)),
        "Acoustic": float(sensor_data.get("Acoustic", sensor_data.get("acoustic", 0.0))),
        "EO_Camera": float(sensor_data.get("EO_Camera", 0.0))
    }

    # 3. Binary Detection Flag: 0 for Bird/No Target, 1 for Target Detected
    if predicted_class == "Bird" or proba < 0.45:
        binary_pred = 0
    else:
        binary_pred = 1

    # 4. Feature Importance Calculation
    importances = XAIEngine.calculate_feature_importances(sensor_data, sensor_scores)
    top_sensors = sorted(
        ["Radar", "Infrared", "Thermal", "Acoustic", "EO_Camera"],
        key=lambda s: importances.get(s, 0.0),
        reverse=True
    )

    # 5. Threat Level Evaluation
    threat_level = XAIEngine.evaluate_threat_level(predicted_class, proba, sensor_data)

    # 6. Uncertainty Calculation
    uncertainty = XAIEngine.calculate_uncertainty(proba, fusion_result)

    # 7. Reasoning and Recommendations
    reasoning, recommendation = XAIEngine.generate_explanation_and_recommendation(
        predicted_class, proba, threat_level, importances, sensor_scores, sensor_data
    )

    # Effective confidence combines model probability with fusion score if present
    effective_confidence = proba
    if fusion_result and "overall_confidence" in fusion_result:
        effective_confidence = round(0.5 * proba + 0.5 * float(fusion_result["overall_confidence"]), 2)

    return {
        # --- LEGACY TUPLE COMPATIBILITY FIELDS ---
        "prediction": binary_pred,
        "confidence": round(effective_confidence, 2),

        # --- EXPLAINABLE AI DIAGNOSTIC FIELDS ---
        "predicted_class": predicted_class,
        "prediction_probability": round(proba, 2),
        "threat_level": threat_level,
        "feature_importance": importances,
        "top_contributing_sensors": top_sensors[:3],
        "reasoning": reasoning,
        "uncertainty": uncertainty,
        "recommendation": recommendation,
        "ai_metadata": {
            "model_type": "RandomForestClassifier + XAI Decision Tree",
            "weather": sensor_data.get("weather", "Clear"),
            "distance_km": sensor_data.get("distance", 25.0),
            "stealth_rating": sensor_data.get("stealth", 0.0)
        }
    }