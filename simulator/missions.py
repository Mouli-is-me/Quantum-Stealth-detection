"""
Mission Templates Module
Defines mission types, operational constraints, expected sensor behaviors, and threat levels.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Any
from simulator.profiles import AircraftType


class ThreatLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class MissionType(Enum):
    COMMERCIAL_FLIGHT = "Commercial Flight"
    CARGO_FLIGHT = "Cargo Flight"
    RECONNAISSANCE = "Reconnaissance Mission"
    STEALTH_PENETRATION = "Stealth Penetration"
    BORDER_SURVEILLANCE = "Border Surveillance"
    DRONE_PATROL = "Drone Patrol"
    CRUISE_MISSILE_ATTACK = "Cruise Missile Attack"
    HELICOPTER_SEARCH = "Helicopter Search"
    BIRD_ACTIVITY = "Bird Activity"
    UNKNOWN_INTRUSION = "Unknown Intrusion"
    SEARCH_AND_RESCUE = "Search and Rescue"
    CUSTOM = "Custom Mission"


@dataclass
class MissionTemplate:
    name: str
    mission_type: MissionType
    typical_altitude_m: Tuple[float, float]
    typical_speed_knots: Tuple[float, float]
    expected_route: str
    expected_sensor_visibility: Dict[str, float]
    threat_level: ThreatLevel
    duration_min: Tuple[float, float]
    primary_aircraft_types: List[AircraftType]
    description: str


MISSION_TEMPLATES: Dict[MissionType, MissionTemplate] = {
    MissionType.COMMERCIAL_FLIGHT: MissionTemplate(
        name="Commercial Flight",
        mission_type=MissionType.COMMERCIAL_FLIGHT,
        typical_altitude_m=(8000.0, 12000.0),
        typical_speed_knots=(420.0, 520.0),
        expected_route="Civilian Air Corridor Waypoint Alpha to Bravo",
        expected_sensor_visibility={"Radar": 0.95, "Infrared": 0.85, "Thermal": 0.85, "Acoustic": 0.30, "EO_Camera": 0.70},
        threat_level=ThreatLevel.LOW,
        duration_min=(120.0, 480.0),
        primary_aircraft_types=[AircraftType.COMMERCIAL],
        description="Standard scheduled passenger airliner transit along designated civilian airways."
    ),
    MissionType.CARGO_FLIGHT: MissionTemplate(
        name="Cargo Flight",
        mission_type=MissionType.CARGO_FLIGHT,
        typical_altitude_m=(7000.0, 11000.0),
        typical_speed_knots=(380.0, 480.0),
        expected_route="Freight Air Route Charlie",
        expected_sensor_visibility={"Radar": 0.95, "Infrared": 0.85, "Thermal": 0.80, "Acoustic": 0.35, "EO_Camera": 0.65},
        threat_level=ThreatLevel.LOW,
        duration_min=(180.0, 600.0),
        primary_aircraft_types=[AircraftType.COMMERCIAL],
        description="Heavy air freight transport operating on fixed trans-continental flight corridors."
    ),
    MissionType.RECONNAISSANCE: MissionTemplate(
        name="Reconnaissance Mission",
        mission_type=MissionType.RECONNAISSANCE,
        typical_altitude_m=(3000.0, 9000.0),
        typical_speed_knots=(120.0, 240.0),
        expected_route="Loiter Pattern over Sector 4",
        expected_sensor_visibility={"Radar": 0.50, "Infrared": 0.40, "Thermal": 0.45, "Acoustic": 0.25, "EO_Camera": 0.55},
        threat_level=ThreatLevel.MEDIUM,
        duration_min=(240.0, 1200.0),
        primary_aircraft_types=[AircraftType.RECON_DRONE],
        description="High-endurance intelligence gathering and ISR loiter mission."
    ),
    MissionType.STEALTH_PENETRATION: MissionTemplate(
        name="Stealth Penetration",
        mission_type=MissionType.STEALTH_PENETRATION,
        typical_altitude_m=(6000.0, 14000.0),
        typical_speed_knots=(550.0, 1100.0),
        expected_route="Tactical Ingress Vector Epsilon",
        expected_sensor_visibility={"Radar": 0.05, "Infrared": 0.30, "Thermal": 0.35, "Acoustic": 0.20, "EO_Camera": 0.40},
        threat_level=ThreatLevel.CRITICAL,
        duration_min=(45.0, 180.0),
        primary_aircraft_types=[AircraftType.STEALTH_FIGHTER],
        description="Deep strike penetration inside defended airspace utilizing RAM stealth coatings and low observables."
    ),
    MissionType.BORDER_SURVEILLANCE: MissionTemplate(
        name="Border Surveillance",
        mission_type=MissionType.BORDER_SURVEILLANCE,
        typical_altitude_m=(1500.0, 5000.0),
        typical_speed_knots=(80.0, 160.0),
        expected_route="Linear Patrol along Border Line Delta",
        expected_sensor_visibility={"Radar": 0.65, "Infrared": 0.55, "Thermal": 0.60, "Acoustic": 0.50, "EO_Camera": 0.75},
        threat_level=ThreatLevel.MEDIUM,
        duration_min=(120.0, 360.0),
        primary_aircraft_types=[AircraftType.RECON_DRONE, AircraftType.HELICOPTER],
        description="Continuous perimeter patrol monitoring international boundary security."
    ),
    MissionType.DRONE_PATROL: MissionTemplate(
        name="Drone Patrol",
        mission_type=MissionType.DRONE_PATROL,
        typical_altitude_m=(2000.0, 6000.0),
        typical_speed_knots=(100.0, 180.0),
        expected_route="Grid Search Area Hotel",
        expected_sensor_visibility={"Radar": 0.45, "Infrared": 0.35, "Thermal": 0.40, "Acoustic": 0.30, "EO_Camera": 0.60},
        threat_level=ThreatLevel.MEDIUM,
        duration_min=(90.0, 300.0),
        primary_aircraft_types=[AircraftType.RECON_DRONE],
        description="Autonomous or remotely piloted UAV patrol over operational grid."
    ),
    MissionType.CRUISE_MISSILE_ATTACK: MissionTemplate(
        name="Cruise Missile Attack",
        mission_type=MissionType.CRUISE_MISSILE_ATTACK,
        typical_altitude_m=(30.0, 200.0),
        typical_speed_knots=(480.0, 620.0),
        expected_route="Low-Altitude Terrain Following Ingress",
        expected_sensor_visibility={"Radar": 0.20, "Infrared": 0.55, "Thermal": 0.65, "Acoustic": 0.65, "EO_Camera": 0.30},
        threat_level=ThreatLevel.CRITICAL,
        duration_min=(15.0, 60.0),
        primary_aircraft_types=[AircraftType.CRUISE_MISSILE],
        description="High-speed terrain-hugging precision missile strike targeting strategic assets."
    ),
    MissionType.HELICOPTER_SEARCH: MissionTemplate(
        name="Helicopter Search",
        mission_type=MissionType.HELICOPTER_SEARCH,
        typical_altitude_m=(100.0, 1000.0),
        typical_speed_knots=(70.0, 140.0),
        expected_route="Low-Level Ridge Line Contour Flight",
        expected_sensor_visibility={"Radar": 0.75, "Infrared": 0.80, "Thermal": 0.85, "Acoustic": 0.95, "EO_Camera": 0.80},
        threat_level=ThreatLevel.HIGH,
        duration_min=(45.0, 150.0),
        primary_aircraft_types=[AircraftType.HELICOPTER],
        description="Tactical rotary-wing search flight at low altitude with high acoustic rotor signature."
    ),
    MissionType.BIRD_ACTIVITY: MissionTemplate(
        name="Bird Activity",
        mission_type=MissionType.BIRD_ACTIVITY,
        typical_altitude_m=(20.0, 500.0),
        typical_speed_knots=(15.0, 40.0),
        expected_route="Random Biological Migration Drift",
        expected_sensor_visibility={"Radar": 0.05, "Infrared": 0.05, "Thermal": 0.10, "Acoustic": 0.05, "EO_Camera": 0.15},
        threat_level=ThreatLevel.LOW,
        duration_min=(10.0, 120.0),
        primary_aircraft_types=[AircraftType.BIRD],
        description="Natural biological flock migration causing radar clutter."
    ),
    MissionType.UNKNOWN_INTRUSION: MissionTemplate(
        name="Unknown Intrusion",
        mission_type=MissionType.UNKNOWN_INTRUSION,
        typical_altitude_m=(500.0, 10000.0),
        typical_speed_knots=(150.0, 700.0),
        expected_route="Erratic Non-Standard Trajectory",
        expected_sensor_visibility={"Radar": 0.50, "Infrared": 0.50, "Thermal": 0.50, "Acoustic": 0.50, "EO_Camera": 0.50},
        threat_level=ThreatLevel.HIGH,
        duration_min=(20.0, 180.0),
        primary_aircraft_types=[AircraftType.UNKNOWN],
        description="Unidentified contact entering restricted airspace without transponder response."
    ),
    MissionType.SEARCH_AND_RESCUE: MissionTemplate(
        name="Search and Rescue",
        mission_type=MissionType.SEARCH_AND_RESCUE,
        typical_altitude_m=(150.0, 1500.0),
        typical_speed_knots=(60.0, 130.0),
        expected_route="Expanding Square Search Pattern",
        expected_sensor_visibility={"Radar": 0.70, "Infrared": 0.75, "Thermal": 0.80, "Acoustic": 0.90, "EO_Camera": 0.85},
        threat_level=ThreatLevel.LOW,
        duration_min=(60.0, 300.0),
        primary_aircraft_types=[AircraftType.HELICOPTER, AircraftType.RECON_DRONE],
        description="Humanitarian emergency search and rescue sweep."
    ),
    MissionType.CUSTOM: MissionTemplate(
        name="Custom Mission",
        mission_type=MissionType.CUSTOM,
        typical_altitude_m=(100.0, 12000.0),
        typical_speed_knots=(50.0, 800.0),
        expected_route="User Configured Custom Waypoints",
        expected_sensor_visibility={"Radar": 0.50, "Infrared": 0.50, "Thermal": 0.50, "Acoustic": 0.50, "EO_Camera": 0.50},
        threat_level=ThreatLevel.MEDIUM,
        duration_min=(30.0, 240.0),
        primary_aircraft_types=[AircraftType.UNKNOWN],
        description="User-defined simulation mission template."
    )
}


def get_mission_template(mission_val: Any) -> MissionTemplate:
    """Retrieve mission template by MissionType enum, string name, or fallback to CUSTOM."""
    if isinstance(mission_val, MissionType):
        return MISSION_TEMPLATES.get(mission_val, MISSION_TEMPLATES[MissionType.CUSTOM])
    if isinstance(mission_val, str):
        for mtype, template in MISSION_TEMPLATES.items():
            if mtype.value.lower() == mission_val.lower() or mtype.name.lower() == mission_val.lower():
                return template
    return MISSION_TEMPLATES[MissionType.CUSTOM]
