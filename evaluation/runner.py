"""
AI Evaluation Runner Module
Main entry point for batch scenario evaluation, robustness testing, benchmarking, and report generation.
"""

import os
from typing import Dict, Any, Optional

from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from fusion.fusion import adaptive_sensor_fusion
from ai.predict import predict_explainable
from evaluation.metrics import PerformanceMetrics
from evaluation.robustness import RobustnessEvaluator
from evaluation.benchmark import FusionBenchmarker
from evaluation.report_generator import EvaluationReportGenerator


def evaluate_ai_system(
    num_scenarios: int = 150,
    seed: int = 42,
    report_path: str = "evaluation/evaluation_report.md"
) -> Dict[str, Any]:
    """
    Executes automated batch scenario evaluation, robustness sweeps, fusion benchmarking,
    and report generation.
    """
    y_true, y_pred, class_true, class_pred, confidences = [], [], [], [], []
    failure_cases = []

    # 1. Batch Scenario Execution
    for i in range(num_scenarios):
        scen_seed = seed + i * 7
        env = generate_environment(seed=scen_seed)
        scores = calculate_sensor_scores(env, seed=scen_seed)

        fusion_res = adaptive_sensor_fusion(scores, env)
        xai_res = predict_explainable({**env, **scores}, fusion_result=fusion_res)

        ground_class = env["ground_truth"].get("true_aircraft_class", env.get("aircraft_type", "Unknown Object"))
        gt_binary = 0 if ground_class == "Bird" else 1

        pred_binary = xai_res["prediction"]
        pred_class = xai_res["predicted_class"]
        conf = xai_res["confidence"]

        y_true.append(gt_binary)
        y_pred.append(pred_binary)
        class_true.append(ground_class)
        class_pred.append(pred_class)
        confidences.append(conf)

        if ground_class != pred_class:
            failure_cases.append({
                "scenario_index": i,
                "ground_truth": ground_class,
                "predicted": pred_class,
                "confidence": conf,
                "weather": env.get("weather"),
                "distance": env.get("distance")
            })

    # 2. Overall Performance Metrics Calculation
    overall_metrics = PerformanceMetrics.calculate_classification_metrics(
        y_true, y_pred, class_true, class_pred, confidences
    )

    # 3. Environmental & Hardware Robustness Sweeps
    env_robustness = RobustnessEvaluator.evaluate_environmental_robustness(
        samples_per_condition=min(20, max(5, num_scenarios // 8)), seed=seed
    )
    fail_robustness = RobustnessEvaluator.evaluate_sensor_failure_robustness(
        samples_per_condition=min(20, max(5, num_scenarios // 8)), seed=seed + 50
    )

    # 4. Comparative Fusion Benchmark
    fusion_bm = FusionBenchmarker.run_fusion_benchmark(
        num_scenarios=min(50, max(15, num_scenarios // 3)), seed=seed + 200
    )

    # 5. Generate Markdown Evaluation Report
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    report_md = EvaluationReportGenerator.generate_markdown_report(
        overall_metrics, env_robustness, fail_robustness, fusion_bm, failure_cases, report_path=report_path
    )

    return {
        "overall_metrics": overall_metrics,
        "environmental_robustness": env_robustness,
        "hardware_robustness": fail_robustness,
        "fusion_benchmark": fusion_bm,
        "failure_case_count": len(failure_cases),
        "report_saved_path": report_path
    }


if __name__ == "__main__":
    res = evaluate_ai_system(num_scenarios=100)
    print(f"Evaluation Completed! Accuracy: {res['overall_metrics']['accuracy']*100:.2f}%. Report saved to: {res['report_saved_path']}")
