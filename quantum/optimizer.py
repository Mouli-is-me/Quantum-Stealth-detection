from quantum.qubo import build_qubo
from quantum.solver import solve_qubo


def optimize_sensors(scores):

    qp = build_qubo(
        scores["Radar"],
        scores["Infrared"],
        scores["Acoustic"]
    )

    result = solve_qubo(qp, scores)

    return result