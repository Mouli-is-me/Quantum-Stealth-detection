import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("data/sensor_dataset.csv")

# Convert weather text to numbers
df["weather"] = df["weather"].map({
    "Clear": 0,
    "Rain": 1,
    "Fog": 2
})

# Features
X = df[[
    "distance",
    "weather",
    "stealth",
    "engine_heat",
    "noise",
    "radar",
    "infrared",
    "acoustic"
]]

# Target
y = df["target"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2%}")

# Save model
joblib.dump(model, "ai/model.pkl")

print("Model saved successfully!")