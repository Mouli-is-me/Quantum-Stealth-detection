from qiskit_optimization import QuadraticProgram


def build_qubo(radar, infrared, acoustic):

    qp = QuadraticProgram()

    qp.binary_var("Radar")
    qp.binary_var("Infrared")
    qp.binary_var("Acoustic")

    penalty = 0.5

    qp.maximize(
        linear={
            "Radar": radar - penalty,
            "Infrared": infrared - penalty,
            "Acoustic": acoustic - penalty
        }
    )

    return qp