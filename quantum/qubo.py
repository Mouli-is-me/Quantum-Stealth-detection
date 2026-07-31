from qiskit_optimization import QuadraticProgram
from typing import Union, Dict, Any

def build_qubo(*args, **kwargs) -> QuadraticProgram:
    """
    Builds a Quadratic Program (QUBO) for sensor selection optimization.
    Supports both legacy positional calls and generalized dictionaries.
    
    Args:
        *args: Either:
               - A single dict: {sensor_name: confidence}
               - Three floats: radar, infrared, acoustic (legacy)
        **kwargs: Optional weights:
                  - w_conf (float): weight for confidence reward. Default 0.6.
                  - w_unc (float): weight for uncertainty penalty. Default 0.4.
                  - w_agree (float): weight for sensor agreement reward. Default 0.3.
                  - w_disagree (float): weight for sensor disagreement penalty. Default 0.7.
                  - selection_penalty (float): penalty for selecting any sensor. Default 0.25.
                  
    Returns:
        QuadraticProgram: The constructed QUBO optimization problem.
    """
    # Parse hyper-parameters from kwargs with defaults
    w_conf = kwargs.pop("w_conf", 0.6)
    w_unc = kwargs.pop("w_unc", 0.4)
    w_agree = kwargs.pop("w_agree", 0.3)
    w_disagree = kwargs.pop("w_disagree", 0.7)
    selection_penalty = kwargs.pop("selection_penalty", 0.25)
    
    # Determine the scores dict from args/kwargs
    scores: Dict[str, float] = {}
    if len(args) == 1 and isinstance(args[0], dict):
        scores = {k: float(v) for k, v in args[0].items() if isinstance(v, (int, float))}
    elif len(args) == 3:
        scores = {
            "Radar": float(args[0]),
            "Infrared": float(args[1]),
            "Acoustic": float(args[2])
        }
    elif "scores" in kwargs:
        scores = {k: float(v) for k, v in kwargs["scores"].items() if isinstance(v, (int, float))}
    else:
        # Check standard names
        for key in ["Radar", "Infrared", "Acoustic"]:
            val = kwargs.get(key) or kwargs.get(key.lower())
            if val is not None:
                scores[key] = val
        if not scores and kwargs:
            scores = {k: v for k, v in kwargs.items() if isinstance(v, (int, float))}
        if not scores and args:
            scores = {f"Sensor_{i}": val for i, val in enumerate(args)}

    qp = QuadraticProgram()
    
    # 1. Define binary variables for each sensor
    sensor_names = list(scores.keys())
    for sensor in sensor_names:
        qp.binary_var(sensor)
        
    # 2. Formulate the Linear Coefficients
    # Reward high confidence (c_i), penalize high uncertainty (u_i = 1 - c_i)
    # Plus selection penalty to prevent picking weak sensors
    linear_coeffs = {}
    for sensor in sensor_names:
        c_i = scores[sensor]
        u_i = 1.0 - c_i
        # alpha_i = w_conf * c_i - w_unc * u_i - selection_penalty
        alpha_i = (w_conf * c_i) - (w_unc * u_i) - selection_penalty
        linear_coeffs[sensor] = alpha_i
        
    # 3. Formulate the Quadratic Coefficients
    # Reward agreement (1 - |c_i - c_j|) and penalize disagreement (|c_i - c_j|)
    quadratic_coeffs = {}
    n = len(sensor_names)
    for i in range(n):
        for j in range(i + 1, n):
            s1, s2 = sensor_names[i], sensor_names[j]
            c1, c2 = scores[s1], scores[s2]
            disagreement = abs(c1 - c2)
            agreement = 1.0 - disagreement
            
            # beta_ij = w_agree * agreement - w_disagree * disagreement
            beta_ij = (w_agree * agreement) - (w_disagree * disagreement)
            quadratic_coeffs[(s1, s2)] = beta_ij
            
    # Maximize the multi-objective utility function
    qp.maximize(
        linear=linear_coeffs,
        quadratic=quadratic_coeffs
    )
    
    return qp