from typing import Dict, List, Any
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import NumPyMinimumEigensolver

from quantum.weights import calculate_fusion_weights
from quantum.explain import generate_explanation

def solve_qubo(qp: QuadraticProgram, sensor_scores: Dict[str, float]) -> Dict[str, Any]:
    """
    Solve the QUBO and return a structured dictionary containing selection,
    weights, energies, confidence scores, matrix representation, bitstring,
    and a dynamic human-readable explanation.
    
    Args:
        qp: The constructed QuadraticProgram (QUBO).
        sensor_scores: Dictionary of sensor confidence scores.
        
    Returns:
        Dict[str, Any]: Rich output including selection, weights, energy, and explanations.
    """
    # 1. Use the NumPy Minimum Eigensolver through Qiskit's MinimumEigenOptimizer
    solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    result = solver.solve(qp)
    
    # 2. Extract selection state
    # result.variables_dict maps variable names (sensor names) to binary values (0.0 or 1.0)
    selection = {
        name: bool(value)
        for name, value in result.variables_dict.items()
    }
    
    selected_sensors = [
        sensor
        for sensor, enabled in selection.items()
        if enabled
    ]
    
    # Clean sensor scores to numeric values
    clean_scores = {k: float(v) for k, v in sensor_scores.items() if isinstance(v, (int, float))}

    # 3. Calculate adaptive fusion weights
    weights = calculate_fusion_weights(clean_scores, selected_sensors)
    
    # 4. Calculate overall fused confidence (weighted average)
    if selected_sensors:
        fusion_score = sum(weights[s] * clean_scores[s] for s in selected_sensors)
    else:
        fusion_score = 0.0
        
    # 5. Extract bitstring
    # The solver returns variables in the order defined in the QP
    bitstring = "".join(str(int(result.x[i])) for i in range(len(result.x)))
    
    # 6. Extract QUBO Matrix Representation for inspectability
    linear_dict = {k: round(v, 4) for k, v in qp.objective.linear.to_dict().items()}
    quadratic_dict = {
        f"{k[0]},{k[1]}": round(v, 4)
        for k, v in qp.objective.quadratic.to_dict().items()
    }
    qubo_matrix = {
        "linear": linear_dict,
        "quadratic": quadratic_dict
    }
    
    # 7. Generate Dynamic Explanation
    explanation = generate_explanation(clean_scores, selected_sensors, weights)
    
    # 8. Return structured dict with legacy fields and new rich fields
    res = {
        # Legacy fields for backward compatibility
        "selection": selection,
        "selected_count": len(selected_sensors),
        "fusion_score": round(fusion_score, 3),
        
        # New rich fields
        "selected_sensors": selected_sensors,
        "weights": weights,
        "energy": round(-result.fval, 3),  # Energy in physics terms is minimized; since QP maximizes, Energy = -fval
        "objective_value": round(result.fval, 3),
        "confidence": round(fusion_score, 3),
        "qubo_matrix": qubo_matrix,
        "bitstring": bitstring,
        "reason": explanation
    }

    # Top-level selection flags for direct key access compatibility
    for sensor_name, is_selected in selection.items():
        if sensor_name not in res:
            res[sensor_name] = is_selected

    return res