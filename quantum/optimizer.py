from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import NumPyMinimumEigensolver

from quantum.qubo import build_qubo


def optimize_sensors(scores):

    qp = build_qubo(
        scores["Radar"],
        scores["Infrared"],
        scores["Acoustic"]
    )

    solver = MinimumEigenOptimizer(
        NumPyMinimumEigensolver()
    )

    result = solver.solve(qp)

    return {
        "Radar": bool(result.variables_dict["Radar"]),
        "Infrared": bool(result.variables_dict["Infrared"]),
        "Acoustic": bool(result.variables_dict["Acoustic"])
    }