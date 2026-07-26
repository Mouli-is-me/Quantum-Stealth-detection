import joblib
import pandas as pd

model = joblib.load("ai/model.pkl")

sample = pd.DataFrame([{
    "distance": 30,
    "weather": 0,      # Clear
    "stealth": 0.3,
    "engine_heat": 0.8,
    "noise": 0.6,
    "radar": 0.75,
    "infrared": 0.65,
    "acoustic": 0.55
}])

prediction = model.predict(sample)[0]
probability = model.predict_proba(sample)[0]

print("Prediction:", "Target Detected" if prediction else "No Target")
print("Confidence:", round(max(probability) * 100, 2), "%")