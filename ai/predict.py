import joblib
import pandas as pd

model = joblib.load("ai/model.pkl")


def predict(sensor_data):

    weather_map = {
        "Clear": 0,
        "Rain": 1,
        "Fog": 2
    }

    df = pd.DataFrame([{
        "distance": sensor_data["distance"],
        "weather": weather_map[sensor_data["weather"]],
        "stealth": sensor_data["stealth"],
        "engine_heat": sensor_data["engine_heat"],
        "noise": sensor_data["noise"],

        "radar": sensor_data["Radar"],
        "infrared": sensor_data["Infrared"],
        "acoustic": sensor_data["Acoustic"]
    }])

    prediction = model.predict(df)[0]
    confidence = model.predict_proba(df)[0].max()

    return prediction, confidence