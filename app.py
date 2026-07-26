from simulator.sensor_simulator import (
    generate_environment,
    calculate_sensor_scores
)

from ai.predict import predict

env = generate_environment()

scores = calculate_sensor_scores(env)

data = {
    **env,
    **scores
}

prediction, confidence = predict(data)

from quantum.optimizer import optimize_sensors

selection = optimize_sensors(scores)

print("\n========== QUANTUM DECISION ==========")

for sensor, enabled in selection.items():

    print(sensor, "->", "ON" if enabled else "OFF")

print("\n========== ENVIRONMENT ==========")

for k, v in env.items():
    print(f"{k:15}: {v}")

print("\n========== SENSOR SCORES ==========")

for k, v in scores.items():
    print(f"{k:15}: {v}")

print("\n========== AI RESULT ==========")

print("Prediction :", "Target" if prediction else "No Target")

print("Confidence :", round(confidence * 100, 2), "%")