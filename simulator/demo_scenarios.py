"""
Predefined Demonstration Scenarios Module
Provides 8 deterministic, engineering-inspired demonstration scenario presets.
"""

from typing import Dict, Any, List
from simulator.profiles import AircraftType
from simulator.environment import Weather, SensorHealth
from simulator.missions import MissionType


DEMO_SCENARIO_PRESETS: Dict[int, Dict[str, Any]] = {
    1: {
        "scenario_id": "DEMO-001",
        "title": "Commercial Aircraft in Clear Weather",
        "aircraft_type": AircraftType.COMMERCIAL,
        "mission_type": MissionType.COMMERCIAL_FLIGHT,
        "weather": Weather.CLEAR_DAY,
        "distance_km": 25.0,
        "jamming_level": 0.0,
        "seed": 1001,
        "description": "Baseline verification scenario: civilian airliner operating under optimal clear day visual/radar tracking conditions."
    },
    2: {
        "scenario_id": "DEMO-002",
        "title": "Stealth Fighter in Heavy Rain",
        "aircraft_type": AircraftType.STEALTH_FIGHTER,
        "mission_type": MissionType.STEALTH_PENETRATION,
        "weather": Weather.HEAVY_RAIN,
        "distance_km": 35.0,
        "jamming_level": 0.0,
        "seed": 1002,
        "description": "Low-observable 5th gen contact penetrating airspace during severe rainstorm RF attenuation."
    },
    3: {
        "scenario_id": "DEMO-003",
        "title": "Recon Drone at Night",
        "aircraft_type": AircraftType.RECON_DRONE,
        "mission_type": MissionType.RECONNAISSANCE,
        "weather": Weather.NIGHT,
        "distance_km": 20.0,
        "jamming_level": 0.0,
        "seed": 1003,
        "description": "Tactical UAV loitering under cover of darkness (low daylight optical contrast, moderate thermal/acoustic)."
    },
    4: {
        "scenario_id": "DEMO-004",
        "title": "Cruise Missile under Electronic Jamming",
        "aircraft_type": AircraftType.CRUISE_MISSILE,
        "mission_type": MissionType.CRUISE_MISSILE_ATTACK,
        "weather": Weather.CLEAR,
        "distance_km": 15.0,
        "jamming_level": 0.85,
        "seed": 1004,
        "description": "High-threat terrain-following missile ingress under heavy active electronic countermeasure jamming."
    },
    5: {
        "scenario_id": "DEMO-005",
        "title": "Bird Causing False Alarm",
        "aircraft_type": AircraftType.BIRD,
        "mission_type": MissionType.BIRD_ACTIVITY,
        "weather": Weather.CLEAR,
        "distance_km": 8.0,
        "jamming_level": 0.0,
        "seed": 1005,
        "description": "Biological clutter contact testing false positive discrimination mechanisms."
    },
    6: {
        "scenario_id": "DEMO-006",
        "title": "Drone Swarm",
        "aircraft_type": AircraftType.RECON_DRONE,
        "mission_type": MissionType.DRONE_PATROL,
        "weather": Weather.CLOUDY,
        "distance_km": 18.0,
        "jamming_level": 0.20,
        "seed": 1006,
        "target_count": 4,
        "description": "Multi-target autonomous UAV swarm ingress across sector grid."
    },
    7: {
        "scenario_id": "DEMO-007",
        "title": "Sensor Failure during Surveillance",
        "aircraft_type": AircraftType.HELICOPTER,
        "mission_type": MissionType.HELICOPTER_SEARCH,
        "weather": Weather.MOUNTAIN_REGION,
        "distance_km": 12.0,
        "jamming_level": 0.0,
        "sensor_health": {"Radar": SensorHealth.OFFLINE, "Thermal": SensorHealth.DEGRADED},
        "seed": 1007,
        "description": "Degraded hardware scenario: Radar array offline with partial thermal camera degradation during mountain sweep."
    },
    8: {
        "scenario_id": "DEMO-008",
        "title": "Multiple Aircraft with Poor Visibility",
        "aircraft_type": AircraftType.STEALTH_FIGHTER,
        "mission_type": MissionType.STEALTH_PENETRATION,
        "weather": Weather.FOG,
        "distance_km": 30.0,
        "jamming_level": 0.30,
        "secondary_type": AircraftType.COMMERCIAL,
        "seed": 1008,
        "description": "Complex multi-contact scenario: Stealth contact ingress masked by nearby commercial airliner footprint under dense fog."
    }
}


def get_demo_preset(preset_id: int) -> Dict[str, Any]:
    """Retrieve predefined demo scenario settings by preset ID (1..8)."""
    return DEMO_SCENARIO_PRESETS.get(preset_id, DEMO_SCENARIO_PRESETS[1])
