from typing import Dict, Any
from quantum.qubo import build_qubo
from quantum.solver import solve_qubo

def optimize_sensors(scores: Dict[str, float]) -> Dict[str, Any]:
    """
    Main entry point for quantum-enhanced sensor fusion optimization.
    Builds the QUBO formulation from the input scores, solves it using Qiskit,
    and returns a structured selection and weighting scheme.
    
    Args:
        scores: A dictionary mapping sensor names (e.g., Radar, Infrared, Acoustic, Lidar)
                to their respective confidence scores.
                
    Returns:
        Dict[str, Any]: Structured dictionary with selected sensors, normalized weights,
                        energies, objective values, and explainability.
    """
    # Build the QUBO formulation (supports any number of sensors in scores)
    qp = build_qubo(scores)
    
    # Solve using the hybrid quantum-classical solver
    result = solve_qubo(qp, scores)
    
    return result