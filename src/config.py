"""
AEGIS-X Centralized System Configuration Module
Centralizes pipeline thresholds, default seeds, logging formats, threat categories, and evaluation defaults.
"""

import os

# Default System Random Seed
DEFAULT_RANDOM_SEED = 42

# Default Evaluation Parameters
DEFAULT_EVALUATION_SCENARIOS = 100
DEFAULT_EVALUATION_REPORT_PATH = os.path.join("evaluation", "evaluation_report.md")

# Default Sensor Distance & Attenuation Bounds
DEFAULT_MIN_DISTANCE_KM = 0.5
DEFAULT_MAX_DISTANCE_KM = 100.0

# Logging Format
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Target Threat Categories
THREAT_CATEGORIES = {
    "CIVILIAN": "Low",
    "MILITARY_STRIKE": "Critical",
    "RECON": "High",
    "CLUTTER": "Low",
    "UNKNOWN": "Medium"
}
