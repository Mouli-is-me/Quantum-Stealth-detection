"""
AEGIS-X End-to-End System Pipeline Orchestrator
Executes the full pipeline: Scenario Engine -> Sensors -> Adaptive Fusion -> Explainable AI -> Quantum Optimization.
"""

from typing import Dict, Any, Optional

from src.logger import get_aegis_logger
from simulator.sensor_simulator import generate_environment, calculate_sensor_scores
from fusion.fusion import adaptive_sensor_fusion
from ai.predict import predict_explainable, predict
from quantum.optimizer import optimize_sensors


def run_full_aegis_pipeline(
    demo_preset: Optional[int] = None,
    aircraft_type: Optional[str] = None,
    weather: Optional[str] = None,
    distance_km: Optional[float] = None,
    jamming_level: Optional[float] = None,
    target_count: int = 1,
    sensor_health: Optional[Dict[str, str]] = None,
    seed: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Executes the end-to-end AEGIS-X pipeline across all 5 core modules + Quantum Optimizer.
    """
    logger = get_aegis_logger("AEGIS-X.Pipeline")
    logger.info("Initializing AEGIS-X End-to-End Execution Pipeline...")

    # Stage 1: Scenario Generation & Environment Setup
    logger.info("Stage 1: Executing Scenario Intelligence Engine...")
    env = generate_environment(
        aircraft_type=aircraft_type,
        weather=weather,
        distance=distance_km,
        seed=seed,
        jamming_level=jamming_level,
        sensor_health=sensor_health,
        demo_preset=demo_preset,
        target_count=target_count
    )
    logger.info(f"Scenario Generated: ID={env.get('scenario_id')}, Aircraft={env.get('aircraft_type')}, Weather={env.get('weather')}, Range={env.get('distance')} km")

    # Stage 2: Physics-Inspired Synthetic Sensor Simulation
    logger.info("Stage 2: Calculating Physics-Based Sensor Confidence Scores...")
    scores = calculate_sensor_scores(env, seed=seed)
    logger.info(f"Sensor Scores Computed -> Radar={scores['Radar']:.2f}, IR={scores['Infrared']:.2f}, Thermal={scores['Thermal']:.2f}, Acoustic={scores['Acoustic']:.2f}, EO_Camera={scores['EO_Camera']:.2f}")

    # Stage 3: Adaptive Multi-Sensor Fusion Engine
    logger.info("Stage 3: Running Adaptive Multi-Sensor Fusion Engine...")
    fusion_result = adaptive_sensor_fusion(scores, env)
    logger.info(f"Fusion Complete -> Score={fusion_result['fusion_score']:.2f}, Confidence={fusion_result['overall_confidence']:.2f}, Primary Sensor={fusion_result['sensor_rankings'][0]}")

    # Stage 4: Explainable AI & Threat Classification
    logger.info("Stage 4: Executing Explainable AI & Threat Classifier...")
    data_payload = {**env, **scores}
    xai_result = predict_explainable(data_payload, fusion_result=fusion_result)
    legacy_pred, legacy_conf = predict(data_payload)
    logger.info(f"XAI Classification -> Target={xai_result['predicted_class']}, Threat={xai_result['threat_level']}, Confidence={xai_result['confidence']*100:.1f}%")

    # Stage 5: Quantum Sensor Optimization
    logger.info("Stage 5: Solving Quantum QUBO Sensor Optimization...")
    quantum_selection = optimize_sensors(scores)
    logger.info(f"Quantum Selection Computed -> {quantum_selection}")

    logger.info("AEGIS-X Pipeline Execution Completed Successfully.")

    return {
        "scenario": env,
        "sensor_scores": scores,
        "fusion": fusion_result,
        "ai": xai_result,
        "legacy_ai": {"prediction": legacy_pred, "confidence": legacy_conf},
        "quantum_selection": quantum_selection
    }
