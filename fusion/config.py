"""
Sensor Fusion Configuration Module
Defines base reliabilities, environmental multipliers, health penalties, and consensus thresholds.
"""

from typing import Dict

# Baseline reliability ratings for sensors under optimal conditions
BASE_RELIABILITIES: Dict[str, float] = {
    "Radar": 0.92,
    "Infrared": 0.86,
    "Thermal": 0.88,
    "Acoustic": 0.68,
    "EO_Camera": 0.84,
}

# Weather multiplier weights for each sensor modality
WEATHER_MODIFIERS: Dict[str, Dict[str, float]] = {
    "Clear": {
        "Radar": 1.0, "Infrared": 1.0, "Thermal": 1.0, "Acoustic": 1.0, "EO_Camera": 1.0
    },
    "Clear Day": {
        "Radar": 1.0, "Infrared": 1.0, "Thermal": 1.0, "Acoustic": 1.0, "EO_Camera": 1.0
    },
    "Cloudy": {
        "Radar": 0.98, "Infrared": 0.95, "Thermal": 0.95, "Acoustic": 1.00, "EO_Camera": 0.85
    },
    "Rain": {
        "Radar": 0.70, "Infrared": 0.90, "Thermal": 0.90, "Acoustic": 0.80, "EO_Camera": 0.60
    },
    "Heavy Rain": {
        "Radar": 0.45, "Infrared": 0.80, "Thermal": 0.80, "Acoustic": 0.60, "EO_Camera": 0.25
    },
    "Fog": {
        "Radar": 0.95, "Infrared": 0.45, "Thermal": 0.55, "Acoustic": 1.00, "EO_Camera": 0.20
    },
    "Night": {
        "Radar": 1.00, "Infrared": 0.90, "Thermal": 0.90, "Acoustic": 1.00, "EO_Camera": 0.20
    },
    "Snow": {
        "Radar": 0.75, "Infrared": 0.85, "Thermal": 0.85, "Acoustic": 0.70, "EO_Camera": 0.45
    },
    "Desert Heat": {
        "Radar": 1.00, "Infrared": 0.70, "Thermal": 0.70, "Acoustic": 0.85, "EO_Camera": 0.95
    },
    "Mountain Region": {
        "Radar": 0.95, "Infrared": 0.95, "Thermal": 0.95, "Acoustic": 0.90, "EO_Camera": 0.95
    },
    "Electronic Jamming": {
        "Radar": 0.25, "Infrared": 1.00, "Thermal": 1.00, "Acoustic": 1.00, "EO_Camera": 0.85
    }
}

# Health status degradation multipliers
HEALTH_PENALTIES: Dict[str, float] = {
    "Healthy": 1.00,
    "Slightly Degraded": 0.80,
    "Degraded": 0.50,
    "Jammed": 0.20,
    "Faulty": 0.10,
    "Offline": 0.00,
}

# Distance-based decay thresholds (km)
DISTANCE_OPTIMAL = 15.0
DISTANCE_LIMIT = 80.0

# Consensus / Disagreement Threshold
DISAGREEMENT_THRESHOLD = 0.28
