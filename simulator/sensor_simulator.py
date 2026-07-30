import random


def generate_environment():
    """
    Generate a simulated battlefield environment.
    """

    return {
        "distance": random.randint(5, 100),       # km
        "weather": random.choice(["Clear", "Rain", "Fog"]),
        "stealth": random.uniform(0, 1),          # 0 = no stealth, 1 = highly stealthy
        "engine_heat": random.uniform(0, 1),
        "noise": random.uniform(0, 1)
    }


def calculate_sensor_scores(env):
    """
    Calculate confidence scores for each sensor.
    """

    distance_factor = max(0.2, 1 - env["distance"] / 100)

    radar = (
        distance_factor
        * (1 - env["stealth"])
        * (0.8 if env["weather"] == "Rain" else 1.0)
    )

    infrared = (
        distance_factor
        * env["engine_heat"]
        * (0.7 if env["weather"] == "Fog" else 1.0)
    )

    acoustic = (
        distance_factor
        * env["noise"]
    )

    lidar = (
        distance_factor
        * (1 - env["stealth"])
        * (0.5 if env["weather"] in ["Rain", "Fog"] else 1.0)
    )

    thermal = (
        distance_factor
        * env["engine_heat"]
        * 0.9  # Thermal is relatively weather resistant
    )

    sonar = (
        distance_factor
        * env["noise"]
        * (0.8 if env["weather"] == "Rain" else 1.0) # Rain affects sonar slightly
    )

    return {
        "Radar": round(min(radar, 1), 2),
        "Infrared": round(min(infrared, 1), 2),
        "Acoustic": round(min(acoustic, 1), 2),
        "Lidar": round(min(lidar, 1), 2),
        "Thermal": round(min(thermal, 1), 2),
        "Sonar": round(min(sonar, 1), 2)
    }


if __name__ == "__main__":

    environment = generate_environment()

    sensors = calculate_sensor_scores(environment)

    print("\n=== Environment ===")

    for key, value in environment.items():
        print(f"{key}: {value}")

    print("\n=== Sensor Scores ===")

    for key, value in sensors.items():
        print(f"{key}: {value}")