"""
Fusion Benchmarking Module
Quantifies performance improvement of Adaptive Multi-Sensor Fusion vs Raw Single-Sensor Baselines.
"""

from typing import Dict, Any, List
from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from fusion.fusion import adaptive_sensor_fusion
from ai.predict import predict_explainable
from evaluation.metrics import PerformanceMetrics


class FusionBenchmarker:
    """Runs comparative benchmarks comparing Raw Single Sensors vs Fused Adaptive Sensors."""

    @staticmethod
    def run_fusion_benchmark(num_scenarios: int = 50, seed: int = 500) -> Dict[str, Any]:
        """
        Executes parallel evaluation on identical scenarios comparing:
        1. Raw Unweighted Averaging
        2. Adaptive Multi-Sensor Fusion Engine
        """
        raw_y_t, raw_y_p, raw_c_t, raw_c_p, raw_confs = [], [], [], [], []
        fused_y_t, fused_y_p, fused_c_t, fused_c_p, fused_confs = [], [], [], [], []

        for i in range(num_scenarios):
            s_seed = seed + i
            env = generate_environment(seed=s_seed)
            scores = calculate_sensor_scores(env, seed=s_seed)

            ground_class = env["ground_truth"].get("true_aircraft_class", env["aircraft_type"])
            gt_binary = 0 if ground_class == "Bird" else 1

            # 1. Raw Unweighted Averaging Prediction
            raw_avg_score = (scores["Radar"] + scores["Infrared"] + scores["Acoustic"]) / 3.0
            raw_data = {**env, **scores}
            raw_xai = predict_explainable(raw_data, fusion_result=None)

            raw_y_t.append(gt_binary)
            raw_y_p.append(raw_xai["prediction"])
            raw_c_t.append(ground_class)
            raw_c_p.append(raw_xai["predicted_class"])
            raw_confs.append(raw_avg_score)

            # 2. Adaptive Multi-Sensor Fusion Engine Prediction
            fusion_res = adaptive_sensor_fusion(scores, env)
            fused_xai = predict_explainable({**env, **scores}, fusion_result=fusion_res)

            fused_y_t.append(gt_binary)
            fused_y_p.append(fused_xai["prediction"])
            fused_c_t.append(ground_class)
            fused_c_p.append(fused_xai["predicted_class"])
            fused_confs.append(fused_xai["confidence"])

        raw_metrics = PerformanceMetrics.calculate_classification_metrics(
            raw_y_t, raw_y_p, raw_c_t, raw_c_p, raw_confs
        )
        fused_metrics = PerformanceMetrics.calculate_classification_metrics(
            fused_y_t, fused_y_p, fused_c_t, fused_c_p, fused_confs
        )

        acc_gain = fused_metrics.get("accuracy", 0.0) - raw_metrics.get("accuracy", 0.0)
        fa_reduction = raw_metrics.get("false_alarm_rate", 0.0) - fused_metrics.get("false_alarm_rate", 0.0)

        return {
            "num_scenarios": num_scenarios,
            "raw_baseline": {
                "accuracy": raw_metrics.get("accuracy", 0.0),
                "precision": raw_metrics.get("precision", 0.0),
                "recall": raw_metrics.get("recall", 0.0),
                "false_alarm_rate": raw_metrics.get("false_alarm_rate", 0.0),
                "f1_score": raw_metrics.get("f1_score", 0.0)
            },
            "adaptive_fusion": {
                "accuracy": fused_metrics.get("accuracy", 0.0),
                "precision": fused_metrics.get("precision", 0.0),
                "recall": fused_metrics.get("recall", 0.0),
                "false_alarm_rate": fused_metrics.get("false_alarm_rate", 0.0),
                "f1_score": fused_metrics.get("f1_score", 0.0)
            },
            "performance_improvement": {
                "accuracy_gain_pct": round(acc_gain * 100.0, 2),
                "false_alarm_reduction_pct": round(fa_reduction * 100.0, 2)
            }
        }
