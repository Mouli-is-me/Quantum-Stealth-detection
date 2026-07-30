from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import NumPyMinimumEigensolver


def solve_qubo(qp, sensor_scores):
    """
    Solve the QUBO and return a structured result.
    """

    solver = MinimumEigenOptimizer(
        NumPyMinimumEigensolver()
    )

    result = solver.solve(qp)

    selection = {
        name: bool(value)
        for name, value in result.variables_dict.items()
    }

    selected = [
        sensor
        for sensor, enabled in selection.items()
        if enabled
    ]

    if selected:
        fusion_score = (
            sum(sensor_scores[s] for s in selected)
            / len(selected)
        )
    else:
        fusion_score = 0.0

    return {
        "selection": selection,
        "selected_sensors": selected,
        "selected_count": len(selected),
        "fusion_score": round(fusion_score, 3),
        "objective_value": round(result.fval, 3)
    }