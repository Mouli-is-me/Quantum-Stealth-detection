from qiskit_optimization import QuadraticProgram


def build_qubo(radar, infrared, acoustic):
    """
    Builds the Quantum Optimization problem for adaptive sensor fusion.

    Variables
    ---------
    Radar      : 1 if radar is selected
    Infrared   : 1 if infrared is selected
    Acoustic   : 1 if acoustic is selected

    Objective
    ---------
    Maximize:
        Sensor Confidence
      - Weak Sensor Penalty
      - Sensor Conflict Penalty
    """

    qp = QuadraticProgram()

    # Binary decision variables
    qp.binary_var("Radar")
    qp.binary_var("Infrared")
    qp.binary_var("Acoustic")

    scores = {
        "Radar": radar,
        "Infrared": infrared,
        "Acoustic": acoustic
    }

    # ------------------------------------------------------------------
    # Linear Reward
    # ------------------------------------------------------------------

    weak_sensor_penalty = 0.25

    linear = {
        sensor: score - weak_sensor_penalty
        for sensor, score in scores.items()
    }

    # ------------------------------------------------------------------
    # Quadratic Conflict Penalty
    #
    # Larger disagreement between two sensors
    # -> larger penalty if both are selected.
    # ------------------------------------------------------------------

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