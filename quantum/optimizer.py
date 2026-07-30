from quantum.qubo import build_qubo
from quantum.solver import solve_qubo


def optimize_sensors(scores):
    """
    Main entry point for quantum sensor optimization.
    """

    qp = build_qubo(
        scores["Radar"],
        scores["Infrared"],
        scores["Acoustic"]
    )

    result = solve_qubo(qp)

    return result