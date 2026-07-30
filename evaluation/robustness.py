"""
Robustness & Stress Testing Module
Evaluates model performance degradation across weather conditions, sensor health failures, and stress scenarios.
"""

from typing import Dict, List, Any
from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from simulator.environment import Weather, SensorHealth
from fusion.fusion import adaptive_sensor_fusion
from ai.predict import predict_explainable
from evaluation.metrics import PerformanceMetrics


class RobustnessEvaluator:
    """Runs environmental and hardware degradation sweeps to measure AI robustness."""

    @staticmethod
    def evaluate_environmental_robustness(samples_per_condition: int = 15, seed: int = 42) -> Dict[str, Any]:
        """
        Measures accuracy and detection rates across distinct weather conditions.
        """
        conditions = [
            Weather.CLEAR_DAY, Weather.HEAVY_RAIN, Weather.FOG,
            Weather.NIGHT, Weather.ELECTRONIC_JAMMING, Weather.DESERT_HEAT
        ]

        results: Dict[str, Any] = {}

        for cond in conditions:
            y_t, y_p, c_t, c_p, confs = [], [], [], [], []

            for i in range(samples_per_condition):
                s_seed = seed + i * 10
                env = generate_environment(weather=cond, seed=s_seed)
                scores = calculate_sensor_scores(env, seed=s_seed)
                fusion_res = adaptive_sensor_fusion(scores, env)
                xai_res = predict_explainable({**env, **scores}, fusion_result=fusion_res)

                ground_class = env["ground_truth"].get("true_aircraft_class", env["aircraft_type"])
                gt_binary = 0 if ground_class == "Bird" else 1

                y_t.append(gt_binary)
                y_p.append(xai_res["prediction"])
                c_t.append(ground_class)
                c_p.append(xai_res["predicted_class"])
                confs.append(xai_res["confidence"])

            m = PerformanceMetrics.calculate_classification_metrics(y_t, y_p, c_t, c_p, confs)
            results[cond.value] = {
                "accuracy": m.get("accuracy", 0.0),
                "detection_rate": m.get("detection_rate", 0.0),
                "false_alarm_rate": m.get("false_alarm_rate", 0.0),
                "avg_confidence": round(sum(confs) / max(1, len(confs)), 3)
            }

        return results

    @staticmethod
    def evaluate_sensor_failure_robustness(samples_per_condition: int = 15, seed: int = 100) -> Dict[str, Any]:
        """
        Measures performance stability under partial or complete hardware sensor failures.
        """
        failure_presets = {
            "All Sensors Healthy": {},
            "Radar Offline": {"Radar": "Offline"},
            "Camera Jammed": {"EO_Camera": "Jammed"},
            "Infrared Degraded": {"Infrared": "Degraded"},
            "Radar & Camera Failed": {"Radar": "Offline", "EO_Camera": "Offline"}
        }

        results: Dict[str, Any] = {}

        for label, health_cfg in failure_presets.items():
            y_t, y_p, c_t, c_p, confs = [], [], [], [], []

            for i in range(samples_per_condition):
                s_seed = seed + i * 10
                env = generate_environment(sensor_health=health_cfg, seed=s_seed)
                scores = calculate_sensor_scores(env, seed=s_seed)
                fusion_res = adaptive_sensor_fusion(scores, env)
                xai_res = predict_explainable({**env, **scores}, fusion_result=fusion_res)

                ground_class = env["ground_truth"].get("true_aircraft_class", env["aircraft_type"])
                gt_binary = 0 if ground_class == "Bird" else 1

                y_t.append(gt_binary)
                y_p.append(xai_res["prediction"])
                c_t.append(ground_class)
                c_p.append(xai_res["predicted_class"])
                confs.append(xai_res["confidence"])

            m = PerformanceMetrics.calculate_classification_metrics(y_t, y_p, c_t, c_p, confs)
            results[label] = {
                "accuracy": m.get("accuracy", 0.0),
                "detection_rate": m.get("detection_rate", 0.0),
                "false_alarm_rate": m.get("false_alarm_rate", 0.0),
                "avg_confidence": round(sum(confs) / max(1, len(confs)), 3)
            }

        return results
