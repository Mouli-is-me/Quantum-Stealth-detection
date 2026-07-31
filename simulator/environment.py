"""
Environment Module
Defines environmental conditions, weather physics, mission profiles, and sensor health states.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any


class Weather(Enum):
    # Extended 20 Weather Types
    CLEAR_SKY = "Clear Sky"
    PARTLY_CLOUDY = "Partly Cloudy"
    CLOUDY = "Cloudy"
    LIGHT_RAIN = "Light Rain"
    HEAVY_RAIN = "Heavy Rain"
    DRIZZLE = "Drizzle"
    THUNDERSTORM = "Thunderstorm"
    MORNING_FOG = "Morning Fog"
    DENSE_FOG = "Dense Fog"
    NIGHT_FOG = "Night Fog"
    SNOW = "Snow"
    HEAVY_SNOW = "Heavy Snow"
    SANDSTORM = "Sandstorm"
    DUST_STORM = "Dust Storm"
    SMOKE = "Smoke"
    HAZE = "Haze"
    CROSS_WIND = "Cross Wind"
    STRONG_WIND = "Strong Wind"
    HUMID = "Humid"
    LOW_VISIBILITY = "Low Visibility"

    # Backward Compatibility Aliases
    CLEAR = "Clear"
    CLEAR_DAY = "Clear Day"
    RAIN = "Rain"
    FOG = "Fog"
    NIGHT = "Night"
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
    weather: Weather = Weather.CLEAR_SKY
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
        if self.weather in [Weather.CLEAR, Weather.CLEAR_SKY, Weather.CLEAR_DAY, Weather.NIGHT, Weather.DESERT_HEAT, Weather.HUMID, Weather.HAZE]:
            return 0.02
        elif self.weather in [Weather.PARTLY_CLOUDY, Weather.CLOUDY]:
            return 0.05
        elif self.weather in [Weather.DRIZZLE, Weather.LIGHT_RAIN, Weather.RAIN]:
            return 0.45
        elif self.weather in [Weather.HEAVY_RAIN, Weather.THUNDERSTORM]:
            return 0.95    # Heavy rain / thunderstorm severe RF attenuation
        elif self.weather in [Weather.MORNING_FOG, Weather.FOG, Weather.DENSE_FOG, Weather.NIGHT_FOG]:
            return 0.18
        elif self.weather in [Weather.SNOW, Weather.HEAVY_SNOW]:
            return 0.40
        elif self.weather in [Weather.SANDSTORM, Weather.DUST_STORM, Weather.SMOKE]:
            return 0.35
        elif self.weather in [Weather.CROSS_WIND, Weather.STRONG_WIND, Weather.LOW_VISIBILITY, Weather.MOUNTAIN_REGION]:
            return 0.08
        elif self.weather == Weather.ELECTRONIC_JAMMING:
            return 0.10
        return 0.02

    def get_ir_extinction_coef(self) -> float:
        """Returns atmospheric IR extinction coefficient per km."""
        base_humidity_loss = (self.humidity_pct / 100.0) * 0.015
        if self.weather in [Weather.CLEAR, Weather.CLEAR_SKY, Weather.CLEAR_DAY, Weather.NIGHT]:
            return 0.01 + base_humidity_loss
        elif self.weather == Weather.DESERT_HEAT:
            return 0.025 + base_humidity_loss
        elif self.weather in [Weather.PARTLY_CLOUDY, Weather.CLOUDY, Weather.HAZE]:
            return 0.035 + base_humidity_loss
        elif self.weather in [Weather.DRIZZLE, Weather.LIGHT_RAIN, Weather.RAIN]:
            return 0.08 + base_humidity_loss
        elif self.weather in [Weather.HEAVY_RAIN, Weather.THUNDERSTORM]:
            return 0.16 + base_humidity_loss
        elif self.weather in [Weather.MORNING_FOG, Weather.FOG, Weather.DENSE_FOG, Weather.NIGHT_FOG]:
            return 0.25 + base_humidity_loss  # Fog scatters MWIR/LWIR strongly
        elif self.weather in [Weather.SNOW, Weather.HEAVY_SNOW]:
            return 0.14 + base_humidity_loss
        elif self.weather in [Weather.SANDSTORM, Weather.DUST_STORM, Weather.SMOKE]:
            return 0.30 + base_humidity_loss  # Particulates scatter IR
        elif self.weather in [Weather.HUMID, Weather.LOW_VISIBILITY]:
            return 0.07 + base_humidity_loss
        return 0.02

    def get_acoustic_absorption_db_per_km(self) -> float:
        """Returns acoustic absorption loss at ~1kHz in dB/km."""
        temp_factor = 1.0 + abs(self.ambient_temp_c - 15.0) * 0.02
        humidity_factor = max(0.5, 1.5 - (self.humidity_pct / 100.0))
        wind_factor = 1.5 if self.weather in [Weather.CROSS_WIND, Weather.STRONG_WIND, Weather.THUNDERSTORM] else 1.0
        return 5.0 * temp_factor * humidity_factor * wind_factor

    def get_optical_visibility_km(self) -> float:
        """Returns effective optical visibility range in km."""
        if self.weather in [Weather.CLEAR, Weather.CLEAR_SKY, Weather.CLEAR_DAY]:
            return min(self.visibility_km, 30.0)
        elif self.weather == Weather.DESERT_HEAT:
            return min(self.visibility_km, 25.0)
        elif self.weather in [Weather.PARTLY_CLOUDY, Weather.HUMID, Weather.HAZE]:
            return min(self.visibility_km, 18.0)
        elif self.weather in [Weather.CLOUDY, Weather.CROSS_WIND, Weather.STRONG_WIND]:
            return min(self.visibility_km, 14.0)
        elif self.weather in [Weather.NIGHT, Weather.NIGHT_FOG]:
            return min(self.visibility_km, 4.0)
        elif self.weather in [Weather.DRIZZLE, Weather.LIGHT_RAIN, Weather.RAIN]:
            return min(self.visibility_km, 8.0)
        elif self.weather in [Weather.HEAVY_RAIN, Weather.THUNDERSTORM]:
            return min(self.visibility_km, 2.5)
        elif self.weather == Weather.MORNING_FOG:
            return min(self.visibility_km, 2.0)
        elif self.weather in [Weather.FOG, Weather.DENSE_FOG, Weather.LOW_VISIBILITY]:
            return min(self.visibility_km, 1.0)
        elif self.weather in [Weather.SNOW, Weather.HEAVY_SNOW]:
            return min(self.visibility_km, 3.0)
        elif self.weather in [Weather.SANDSTORM, Weather.DUST_STORM, Weather.SMOKE]:
            return min(self.visibility_km, 1.5)
        elif self.weather == Weather.MOUNTAIN_REGION:
            return min(self.visibility_km, 18.0)
        return self.visibility_km


def parse_weather(weather_val: Any) -> Weather:
    """Helper to convert string or Weather enum to Weather enum."""
    if isinstance(weather_val, Weather):
        return weather_val
    if isinstance(weather_val, str):
        # Direct match check
        for w in Weather:
            if w.value.lower() == weather_val.lower() or w.name.lower() == weather_val.lower():
                return w
        # Fallback partial matching
        val_lower = weather_val.lower()
        if "clear" in val_lower:
            return Weather.CLEAR_SKY
        elif "rain" in val_lower or "drizzle" in val_lower:
            return Weather.HEAVY_RAIN if "heavy" in val_lower else Weather.LIGHT_RAIN
        elif "fog" in val_lower:
            return Weather.DENSE_FOG if "dense" in val_lower else Weather.MORNING_FOG
        elif "snow" in val_lower:
            return Weather.SNOW
        elif "storm" in val_lower:
            return Weather.THUNDERSTORM
    return Weather.CLEAR_SKY


def parse_sensor_health(health_val: Any) -> SensorHealth:
    """Helper to convert string or SensorHealth enum to SensorHealth enum."""
    if isinstance(health_val, SensorHealth):
        return health_val
    if isinstance(health_val, str):
        for h in SensorHealth:
            if h.value.lower() == health_val.lower() or h.name.lower() == health_val.lower():
                return h
    return SensorHealth.HEALTHY
