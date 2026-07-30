from qiskit_optimization import QuadraticProgram


def build_qubo(radar, infrared, acoustic):
    

    qp = QuadraticProgram()

    qp.binary_var("Radar")
    qp.binary_var("Infrared")
    qp.binary_var("Acoustic")

    scores = {
        "Radar": radar,
        "Infrared": infrared,
        "Acoustic": acoustic
    }


    weak_sensor_penalty = 0.25

    linear = {
        sensor: score - weak_sensor_penalty
        for sensor, score in scores.items()
    }


    quadratic = {
        ("Radar", "Infrared"): abs(radar - infrared),
        ("Radar", "Acoustic"): abs(radar - acoustic),
        ("Infrared", "Acoustic"): abs(infrared - acoustic),
    }

    qp.maximize(
        linear=linear,
        quadratic={
            pair: -value
            for pair, value in quadratic.items()
        }
    )

    return qp