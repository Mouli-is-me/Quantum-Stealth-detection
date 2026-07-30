"""
Explainable AI Engine Module
Provides interpretable ML classification, feature importance attribution, threat level assessment,
uncertainty analysis, systematic reasoning, and tactical recommendations.
"""

import math
from typing import Dict, Any, List, Tuple, Optional


class XAIEngine:
    """Core Explainable AI engine for threat classification and decision attribution."""

    @staticmethod
    def classify_target_type(sensor_data: Dict[str, Any]) -> Tuple[str, float]:
        """
        Classifies contact into one of 7 target classes based on physical features.
        Returns: (predicted_class_name, class_probability)
        """
        # If aircraft_type is explicitly provided in metadata, use it as ground truth baseline
        aircraft_name = sensor_data.get("aircraft_type")
        if aircraft_name:
            if "Commercial" in aircraft_name:
                return "Commercial Aircraft", 0.98
            elif "Stealth" in aircraft_name:
                return "Stealth Fighter", 0.95
            elif "Recon" in aircraft_name or "Drone" in aircraft_name:
                return "Recon Drone", 0.94
            elif "Missile" in aircraft_name:
                return "Cruise Missile", 0.97
            elif "Helicopter" in aircraft_name:
                return "Helicopter", 0.96
            elif "Bird" in aircraft_name:
                return "Bird", 0.99

        # Rule-based decision tree fallback on physical parameters
        stealth = float(sensor_data.get("stealth", 0.1))
        speed = float(sensor_data.get("speed", 300.0))
        altitude = float(sensor_data.get("altitude", 5000.0))
        rcs = float(sensor_data.get("_rcs_m2", 1.0))
        noise = float(sensor_data.get("noise", 0.5))
        heat = float(sensor_data.get("engine_heat", 0.5))

        if rcs < 0.05 and stealth > 0.8:
            return "Stealth Fighter", 0.93
        elif altitude < 300.0 and speed > 400.0:
            return "Cruise Missile", 0.95
        elif rcs < 0.03 and speed < 50.0:
            return "Bird", 0.98
        elif rcs > 10.0 and speed > 350.0:
            return "Commercial Aircraft", 0.96
        elif noise > 0.75 and altitude < 2000.0:
            return "Helicopter", 0.92
        elif rcs < 1.0 and speed < 250.0:
            return "Recon Drone", 0.91

        return "Unknown Object", 0.75

    @staticmethod
    def calculate_feature_importances(
        sensor_data: Dict[str, Any],
        sensor_scores: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Computes relative feature importances for decision attribution.
        Normalizes feature contributions to sum to 1.0 (100%).
        """
        raw_imp = {
            "Radar": float(sensor_scores.get("Radar", 0.5)) * (1.0 - float(sensor_data.get("stealth", 0.1))),
            "Infrared": float(sensor_scores.get("Infrared", 0.5)) * float(sensor_data.get("engine_heat", 0.5)),
            "Thermal": float(sensor_scores.get("Thermal", 0.5)),
            "Acoustic": float(sensor_scores.get("Acoustic", 0.5)) * float(sensor_data.get("noise", 0.5)),
            "EO_Camera": float(sensor_scores.get("EO_Camera", 0.5)),
            "Distance": max(0.1, 1.0 - float(sensor_data.get("distance", 25.0)) / 100.0),
            "Weather": 0.8 if sensor_data.get("weather") == "Clear" else 0.4,
            "Sensor_Health": 0.9
        }

        total = sum(raw_imp.values())
        if total > 0:
            return {k: round(v / total, 3) for k, v in raw_imp.items()}
        return {k: 0.125 for k in raw_imp}

    @staticmethod
    def evaluate_threat_level(
        predicted_class: str,
        confidence: float,
        sensor_data: Dict[str, Any]
    ) -> str:
        """
        Evaluates contextual threat category: 'Low', 'Medium', 'High', 'Critical'.
        """
        stealth = float(sensor_data.get("stealth", 0.0))
        speed = float(sensor_data.get("speed", 0.0))
        dist = float(sensor_data.get("distance", 50.0))

        if predicted_class in ["Cruise Missile", "Stealth Fighter"]:
            if dist < 30.0 or speed > 500.0 or stealth > 0.7:
                return "Critical"
            return "High"
        elif predicted_class in ["Recon Drone", "Helicopter", "Unknown Object"]:
            if dist < 20.0:
                return "High"
            return "Medium"
        elif predicted_class == "Commercial Aircraft":
            return "Low"
        elif predicted_class == "Bird":
            return "Low"

        return "Medium"

    @staticmethod
    def calculate_uncertainty(
        probability: float,
        fusion_result: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculates prediction uncertainty based on model probability entropy and fusion metrics.
        """
        # Model entropy uncertainty
        p = max(0.01, min(0.99, probability))
        entropy = - (p * math.log2(p) + (1 - p) * math.log2(1 - p))
        
        fusion_uncertainty = 0.0
        if fusion_result and "uncertainty" in fusion_result:
            fusion_uncertainty = float(fusion_result["uncertainty"])

        combined_uncertainty = 0.6 * entropy + 0.4 * fusion_uncertainty
        return round(max(0.0, min(1.0, combined_uncertainty)), 2)

    @classmethod
    def generate_explanation_and_recommendation(
        cls,
        predicted_class: str,
        probability: float,
        threat_level: str,
        importances: Dict[str, float],
        sensor_scores: Dict[str, float],
        sensor_data: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Generates systematic diagnostic reasoning and tactical recommendation.
        Returns: (reasoning_text, recommendation_text)
        """
        top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:3]
        top_str = ", ".join([f"{k} ({v*100:.1f}%)" for k, v in top_features])

        weath = sensor_data.get("weather", "Clear")
        dist = sensor_data.get("distance", 25.0)

        reasoning = (
            f"Target classified as '{predicted_class}' with {probability*100:.1f}% confidence. "
            f"Primary decision factors: {top_str}. "
            f"Observed key signatures: Radar score {sensor_scores.get('Radar', 0):.2f}, "
            f"Infrared score {sensor_scores.get('Infrared', 0):.2f}, "
            f"Thermal score {sensor_scores.get('Thermal', 0):.2f} under {weath} conditions at {dist:.1f} km range."
        )

        if threat_level == "Critical":
            rec = "CRITICAL THREAT: Immediately engage automated target tracking and request defensive air cover authorization."
        elif threat_level == "High":
            rec = "HIGH THREAT: Maintain continuous multi-sensor tracking and prime defensive countermeasure systems."
        elif threat_level == "Medium":
            rec = "MEDIUM THREAT: Monitor target flight vector and establish perimeter surveillance baseline."
        else:  # Low
            rec = "LOW THREAT / CIVILIAN CONTACT: Log flight parameters and maintain standard airway monitoring."

        return reasoning, rec
