import pandas as pd
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulator.sensor_simulator import generate_environment, calculate_sensor_scores

dataset = []

for _ in range(1000):

    env = generate_environment()
    sensors = calculate_sensor_scores(env)

    score = (
        sensors["Radar"] +
        sensors["Infrared"] +
        sensors["Acoustic"]
    )

    target_detected = 1 if score > 1.0 else 0

    dataset.append({
        "distance": env["distance"],
        "weather": env["weather"],
        "stealth": env["stealth"],
        "engine_heat": env["engine_heat"],
        "noise": env["noise"],

        "radar": sensors["Radar"],
        "infrared": sensors["Infrared"],
        "acoustic": sensors["Acoustic"],

        "target": target_detected
    })

df = pd.DataFrame(dataset)

df.to_csv("data/sensor_dataset.csv", index=False)

print("Dataset generated successfully!")
print(df.head())