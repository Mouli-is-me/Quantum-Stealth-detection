"""
Environment Module
Defines environmental conditions, weather physics, mission profiles, and sensor health states.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any


class Weather(Enum):
    CLEAR = "Clear"
    CLEAR_DAY = "Clear Day"
    CLOUDY = "Cloudy"
    RAIN = "Rain"
    HEAVY_RAIN = "Heavy Rain"
    FOG = "Fog"
    NIGHT = "Night"
    SNOW = "Snow"
    DESERT_HEAT = "Desert Heat"
    MOUNTAIN_REGION = "Mountain Region"
    ELECTRONIC_JAMMING = "Electronic Jamming"


class SensorHealth(Enum):
    HEALTHY = "Healthy"
    SLIGHTLY_DEGRADED = "Slightly Degraded"
    DEGRADED = "Degraded"
    JAMMED = "Jammed"
    FAULTY = "Faulty"
    OFFLINE = "Offline"


class MissionType(Enum):
    PATROL = "Patrol"
    INFILTRATION = "Infiltration"
    RECONNAISSANCE = "Reconnaissance"
    TRANSIT = "Transit"
    INTERCEPT = "Intercept"


# Health Multipliers: (Signal Confidence Factor, Added Noise Multiplier)
HEALTH_MULTIPLIERS: Dict[SensorHealth, tuple] = {
    SensorHealth.HEALTHY: (1.00, 1.0),
    SensorHealth.SLIGHTLY_DEGRADED: (0.85, 1.25),
    SensorHealth.DEGRADED: (0.60, 1.80),
    SensorHealth.JAMMED: (0.25, 3.50),
    SensorHealth.FAULTY: (0.10, 5.00),
    SensorHealth.OFFLINE: (0.00, 0.0),
}


@dataclass
class EnvironmentConfig:
    distance_km: float = 25.0
    weather: Weather = Weather.CLEAR
    ambient_temp_c: float = 15.0
    humidity_pct: float = 50.0
    visibility_km: float = 20.0
    jamming_level: float = 0.0     # 0.0 (None) to 1.0 (Heavy jamming)
    heading_deg: float = 180.0
    mission_type: Any = MissionType.PATROL
    sensor_health: Dict[str, SensorHealth] = field(default_factory=lambda: {
        "Radar": SensorHealth.HEALTHY,
        "Infrared": SensorHealth.HEALTHY,
        "Thermal": SensorHealth.HEALTHY,
        "Acoustic": SensorHealth.HEALTHY,
        "EO_Camera": SensorHealth.HEALTHY,
    })

    def get_rf_attenuation_db_per_km(self) -> float:
        """Returns X/Ku band radar atmospheric attenuation in dB/km."""
        if self.weather in [Weather.CLEAR, Weather.CLEAR_DAY, Weather.NIGHT, Weather.DESERT_HEAT]:
            return 0.02
        elif self.weather == Weather.CLOUDY:
            return 0.05
        elif self.weather == Weather.RAIN:
            return 0.45
        elif self.weather == Weather.HEAVY_RAIN:
            return 0.85    # Heavy rain severe RF attenuation
        elif self.weather == Weather.FOG:
            return 0.15
        elif self.weather == Weather.SNOW:
            return 0.30
        elif self.weather == Weather.MOUNTAIN_REGION:
            return 0.08
        elif self.weather == Weather.ELECTRONIC_JAMMING:
            return 0.10
        return 0.02

    def get_ir_extinction_coef(self) -> float:
        """Returns atmospheric IR extinction coefficient per km."""
        base_humidity_loss = (self.humidity_pct / 100.0) * 0.015
        if self.weather in [Weather.CLEAR, Weather.CLEAR_DAY, Weather.NIGHT]:
            return 0.01 + base_humidity_loss
        elif self.weather == Weather.DESERT_HEAT:
            return 0.025 + base_humidity_loss  # Thermal shimmer / convection loss
        elif self.weather == Weather.CLOUDY:
            return 0.03 + base_humidity_loss
        elif self.weather == Weather.RAIN:
            return 0.08 + base_humidity_loss
        elif self.weather == Weather.HEAVY_RAIN:
            return 0.15 + base_humidity_loss
        elif self.weather == Weather.FOG:
            return 0.22 + base_humidity_loss  # Dense fog scatters MWIR/LWIR strongly
        elif self.weather == Weather.SNOW:
            return 0.12 + base_humidity_loss
        elif self.weather == Weather.MOUNTAIN_REGION:
            return 0.015 + base_humidity_loss
        return 0.01

    def get_acoustic_absorption_db_per_km(self) -> float:
        """Returns acoustic absorption loss at ~1kHz in dB/km."""
        temp_factor = 1.0 + abs(self.ambient_temp_c - 15.0) * 0.02
        humidity_factor = max(0.5, 1.5 - (self.humidity_pct / 100.0))
        return 5.0 * temp_factor * humidity_factor

    def get_optical_visibility_km(self) -> float:
        """Returns effective optical visibility range in km."""
        if self.weather in [Weather.CLEAR, Weather.CLEAR_DAY]:
            return min(self.visibility_km, 30.0)
        elif self.weather == Weather.DESERT_HEAT:
            return min(self.visibility_km, 25.0)
        elif self.weather == Weather.CLOUDY:
            return min(self.visibility_km, 15.0)
        elif self.weather == Weather.NIGHT:
            return min(self.visibility_km, 5.0)
        elif self.weather == Weather.RAIN:
            return min(self.visibility_km, 8.0)
        elif self.weather == Weather.HEAVY_RAIN:
            return min(self.visibility_km, 3.0)
        elif self.weather == Weather.FOG:
            return min(self.visibility_km, 1.2)
        elif self.weather == Weather.SNOW:
            return min(self.visibility_km, 4.0)
        elif self.weather == Weather.MOUNTAIN_REGION:
            return min(self.visibility_km, 18.0)
        return self.visibility_km


def parse_weather(weather_val: Any) -> Weather:
    """Helper to convert string or Weather enum to Weather enum."""
    if isinstance(weather_val, Weather):
        return weather_val
    if isinstance(weather_val, str):
        for w in Weather:
            if w.value.lower() == weather_val.lower() or w.name.lower() == weather_val.lower():
                return w
    return Weather.CLEAR


def parse_sensor_health(health_val: Any) -> SensorHealth:
    """Helper to convert string or SensorHealth enum to SensorHealth enum."""
    if isinstance(health_val, SensorHealth):
        return health_val
    if isinstance(health_val, str):
        for h in SensorHealth:
            if h.value.lower() == health_val.lower() or h.name.lower() == health_val.lower():
                return h
    return SensorHealth.HEALTHY
