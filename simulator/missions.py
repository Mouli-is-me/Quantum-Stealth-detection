"""
Mission Templates Module
Defines mission types, operational constraints, expected sensor behaviors, and threat levels.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Any
from simulator.profiles import AircraftType


class ThreatLevel(Enum):
    MINIMAL = "Minimal"
    LOW = "Low"
    GUARDED = "Guarded"
    ELEVATED = "Elevated"
    MEDIUM = "Medium"
    SIGNIFICANT = "Significant"
    HIGH = "High"
    CRITICAL = "Critical"
    SEVERE = "Severe"
    EXTREME = "Extreme"


class MissionType(Enum):
    RECONNAISSANCE = "Reconnaissance"
    BORDER_PATROL = "Border Patrol"
    COMBAT_PATROL = "Combat Patrol"
    STRIKE_MISSION = "Strike Mission"
    NAVAL_PATROL = "Naval Patrol"
    ELECTRONIC_WARFARE = "Electronic Warfare"
    SEARCH_AND_RESCUE = "Search and Rescue"
    CARGO_TRANSPORT = "Cargo Transport"
    ESCORT_MISSION = "Escort Mission"
    TRAINING_FLIGHT = "Training Flight"
    SURVEILLANCE = "Surveillance"
    EMERGENCY_RESPONSE = "Emergency Response"
    COVERT_MISSION = "Covert Mission"
    INTELLIGENCE_GATHERING = "Intelligence Gathering"
    AIR_INTERCEPT = "Air Intercept"

    # Backward Compatibility Aliases
    COMMERCIAL_FLIGHT = "Commercial Flight"
    CARGO_FLIGHT = "Cargo Flight"
    STEALTH_PENETRATION = "Stealth Penetration"
    BORDER_SURVEILLANCE = "Border Surveillance"
    DRONE_PATROL = "Drone Patrol"
    CRUISE_MISSILE_ATTACK = "Cruise Missile Attack"
    HELICOPTER_SEARCH = "Helicopter Search"
    BIRD_ACTIVITY = "Bird Activity"
    UNKNOWN_INTRUSION = "Unknown Intrusion"
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
    MissionType.RECONNAISSANCE: MissionTemplate(
        name="Reconnaissance",
        mission_type=MissionType.RECONNAISSANCE,
        typical_altitude_m=(3000.0, 9000.0),
        typical_speed_knots=(120.0, 240.0),
        expected_route="Loiter Pattern over Sector 4",
        expected_sensor_visibility={"Radar": 0.50, "Infrared": 0.40, "Thermal": 0.45, "Acoustic": 0.25, "EO_Camera": 0.55},
        threat_level=ThreatLevel.SIGNIFICANT,
        duration_min=(240.0, 1200.0),
        primary_aircraft_types=[AircraftType.RECON_DRONE, AircraftType.MILITARY_UAV],
        description="High-endurance intelligence gathering and ISR loiter mission."
    ),
    MissionType.BORDER_PATROL: MissionTemplate(
        name="Border Patrol",
        mission_type=MissionType.BORDER_PATROL,
        typical_altitude_m=(1500.0, 5000.0),
        typical_speed_knots=(80.0, 160.0),
        expected_route="Linear Patrol along Border Line Delta",
        expected_sensor_visibility={"Radar": 0.65, "Infrared": 0.55, "Thermal": 0.60, "Acoustic": 0.50, "EO_Camera": 0.75},
        threat_level=ThreatLevel.ELEVATED,
        duration_min=(120.0, 360.0),
        primary_aircraft_types=[AircraftType.RECON_DRONE, AircraftType.HELICOPTER, AircraftType.ATTACK_HELICOPTER],
        description="Perimeter patrol monitoring international boundary security."
    ),
    MissionType.COMBAT_PATROL: MissionTemplate(
        name="Combat Patrol",
        mission_type=MissionType.COMBAT_PATROL,
        typical_altitude_m=(4000.0, 12000.0),
        typical_speed_knots=(350.0, 750.0),
        expected_route="Combat Air Patrol Orbit Sector Echo",
        expected_sensor_visibility={"Radar": 0.70, "Infrared": 0.65, "Thermal": 0.70, "Acoustic": 0.35, "EO_Camera": 0.60},
        threat_level=ThreatLevel.HIGH,
        duration_min=(90.0, 300.0),
        primary_aircraft_types=[AircraftType.FIGHTER_JET, AircraftType.STEALTH_FIGHTER, AircraftType.COMBAT_UAV],
        description="Tactical armed combat patrol holding offensive or defensive readiness."
    ),
    MissionType.STRIKE_MISSION: MissionTemplate(
        name="Strike Mission",
        mission_type=MissionType.STRIKE_MISSION,
        typical_altitude_m=(50.0, 14000.0),
        typical_speed_knots=(500.0, 1100.0),
        expected_route="Tactical Ingress Corridor Foxtrot",
        expected_sensor_visibility={"Radar": 0.25, "Infrared": 0.45, "Thermal": 0.50, "Acoustic": 0.40, "EO_Camera": 0.35},
        threat_level=ThreatLevel.SEVERE,
        duration_min=(30.0, 180.0),
        primary_aircraft_types=[AircraftType.STEALTH_FIGHTER, AircraftType.CRUISE_MISSILE, AircraftType.BOMBER, AircraftType.COMBAT_UAV],
        description="Precision tactical strike ingress targeting fortified assets."
    ),
    MissionType.NAVAL_PATROL: MissionTemplate(
        name="Naval Patrol",
        mission_type=MissionType.NAVAL_PATROL,
        typical_altitude_m=(500.0, 4000.0),
        typical_speed_knots=(150.0, 320.0),
        expected_route="Maritime Search Grid Golf",
        expected_sensor_visibility={"Radar": 0.85, "Infrared": 0.60, "Thermal": 0.65, "Acoustic": 0.45, "EO_Camera": 0.70},
        threat_level=ThreatLevel.MEDIUM,
        duration_min=(180.0, 600.0),
        primary_aircraft_types=[AircraftType.MILITARY_UAV, AircraftType.HELICOPTER, AircraftType.RECON_DRONE],
        description="Maritime reconnaissance and anti-surface surveillance sweep."
    ),
    MissionType.ELECTRONIC_WARFARE: MissionTemplate(
        name="Electronic Warfare",
        mission_type=MissionType.ELECTRONIC_WARFARE,
        typical_altitude_m=(6000.0, 13000.0),
        typical_speed_knots=(350.0, 650.0),
        expected_route="Standoff Jamming Orbit Range",
        expected_sensor_visibility={"Radar": 0.15, "Infrared": 0.35, "Thermal": 0.40, "Acoustic": 0.20, "EO_Camera": 0.45},
        threat_level=ThreatLevel.CRITICAL,
        duration_min=(120.0, 360.0),
        primary_aircraft_types=[AircraftType.STEALTH_FIGHTER, AircraftType.MILITARY_UAV, AircraftType.FIGHTER_JET],
        description="Active RF spectrum jamming and radar suppression operation."
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
        primary_aircraft_types=[AircraftType.HELICOPTER, AircraftType.CARGO_DRONE, AircraftType.QUADCOPTER],
        description="Humanitarian emergency search and recovery sweep."
    ),
    MissionType.CARGO_TRANSPORT: MissionTemplate(
        name="Cargo Transport",
        mission_type=MissionType.CARGO_TRANSPORT,
        typical_altitude_m=(7000.0, 11000.0),
        typical_speed_knots=(380.0, 480.0),
        expected_route="Freight Air Corridor Waypoint Charlie",
        expected_sensor_visibility={"Radar": 0.95, "Infrared": 0.85, "Thermal": 0.80, "Acoustic": 0.35, "EO_Camera": 0.65},
        threat_level=ThreatLevel.GUARDED,
        duration_min=(180.0, 600.0),
        primary_aircraft_types=[AircraftType.CARGO_AIRCRAFT, AircraftType.COMMERCIAL, AircraftType.CARGO_DRONE],
        description="Heavy strategic logistics transport."
    ),
    MissionType.ESCORT_MISSION: MissionTemplate(
        name="Escort Mission",
        mission_type=MissionType.ESCORT_MISSION,
        typical_altitude_m=(5000.0, 12000.0),
        typical_speed_knots=(380.0, 550.0),
        expected_route="High-Altitude Convoy Protective Envelope",
        expected_sensor_visibility={"Radar": 0.80, "Infrared": 0.70, "Thermal": 0.75, "Acoustic": 0.30, "EO_Camera": 0.65},
        threat_level=ThreatLevel.HIGH,
        duration_min=(90.0, 360.0),
        primary_aircraft_types=[AircraftType.FIGHTER_JET, AircraftType.STEALTH_FIGHTER, AircraftType.ATTACK_HELICOPTER],
        description="Armed air defense escort guarding valuable air assets."
    ),
    MissionType.TRAINING_FLIGHT: MissionTemplate(
        name="Training Flight",
        mission_type=MissionType.TRAINING_FLIGHT,
        typical_altitude_m=(2000.0, 8000.0),
        typical_speed_knots=(150.0, 400.0),
        expected_route="Designated Military Training Airspace Zone",
        expected_sensor_visibility={"Radar": 0.85, "Infrared": 0.70, "Thermal": 0.75, "Acoustic": 0.40, "EO_Camera": 0.80},
        threat_level=ThreatLevel.MINIMAL,
        duration_min=(45.0, 180.0),
        primary_aircraft_types=[AircraftType.BUSINESS_JET, AircraftType.CIVILIAN_DRONE, AircraftType.PASSENGER_AIRCRAFT],
        description="Routine flight instruction and evaluation exercise."
    ),
    MissionType.SURVEILLANCE: MissionTemplate(
        name="Surveillance",
        mission_type=MissionType.SURVEILLANCE,
        typical_altitude_m=(1000.0, 6000.0),
        typical_speed_knots=(80.0, 200.0),
        expected_route="Target Sector Continuous Monitoring",
        expected_sensor_visibility={"Radar": 0.60, "Infrared": 0.50, "Thermal": 0.55, "Acoustic": 0.35, "EO_Camera": 0.70},
        threat_level=ThreatLevel.ELEVATED,
        duration_min=(120.0, 480.0),
        primary_aircraft_types=[AircraftType.RECON_DRONE, AircraftType.QUADCOPTER, AircraftType.MILITARY_UAV],
        description="Persistent tactical visual and thermal observation."
    ),
    MissionType.EMERGENCY_RESPONSE: MissionTemplate(
        name="Emergency Response",
        mission_type=MissionType.EMERGENCY_RESPONSE,
        typical_altitude_m=(300.0, 3000.0),
        typical_speed_knots=(100.0, 250.0),
        expected_route="Direct Priority Transit Vector",
        expected_sensor_visibility={"Radar": 0.75, "Infrared": 0.75, "Thermal": 0.80, "Acoustic": 0.70, "EO_Camera": 0.80},
        threat_level=ThreatLevel.MINIMAL,
        duration_min=(30.0, 120.0),
        primary_aircraft_types=[AircraftType.HELICOPTER, AircraftType.CARGO_DRONE],
        description="High-priority medical or disaster intervention flight."
    ),
    MissionType.COVERT_MISSION: MissionTemplate(
        name="Covert Mission",
        mission_type=MissionType.COVERT_MISSION,
        typical_altitude_m=(50.0, 14000.0),
        typical_speed_knots=(400.0, 1000.0),
        expected_route="Low-Observable Infiltration Vector",
        expected_sensor_visibility={"Radar": 0.05, "Infrared": 0.20, "Thermal": 0.25, "Acoustic": 0.15, "EO_Camera": 0.30},
        threat_level=ThreatLevel.EXTREME,
        duration_min=(30.0, 240.0),
        primary_aircraft_types=[AircraftType.STEALTH_FIGHTER, AircraftType.COMBAT_UAV, AircraftType.CRUISE_MISSILE],
        description="Classified stealth insertion or intelligence extraction inside hostile territory."
    ),
    MissionType.INTELLIGENCE_GATHERING: MissionTemplate(
        name="Intelligence Gathering",
        mission_type=MissionType.INTELLIGENCE_GATHERING,
        typical_altitude_m=(5000.0, 15000.0),
        typical_speed_knots=(200.0, 500.0),
        expected_route="SIGINT Standoff Boundary Vector",
        expected_sensor_visibility={"Radar": 0.40, "Infrared": 0.35, "Thermal": 0.40, "Acoustic": 0.15, "EO_Camera": 0.50},
        threat_level=ThreatLevel.SIGNIFICANT,
        duration_min=(240.0, 900.0),
        primary_aircraft_types=[AircraftType.MILITARY_UAV, AircraftType.RECON_DRONE, AircraftType.BUSINESS_JET],
        description="Signals intelligence and multi-spectral electronic data capture."
    ),
    MissionType.AIR_INTERCEPT: MissionTemplate(
        name="Air Intercept",
        mission_type=MissionType.AIR_INTERCEPT,
        typical_altitude_m=(3000.0, 14000.0),
        typical_speed_knots=(600.0, 1200.0),
        expected_route="High-Speed Scramble Vector Kilo",
        expected_sensor_visibility={"Radar": 0.80, "Infrared": 0.75, "Thermal": 0.80, "Acoustic": 0.40, "EO_Camera": 0.65},
        threat_level=ThreatLevel.EXTREME,
        duration_min=(20.0, 90.0),
        primary_aircraft_types=[AircraftType.FIGHTER_JET, AircraftType.STEALTH_FIGHTER],
        description="Emergency scramble intercept targeting unknown airborne threat."
    ),
}


def get_mission_template(mission_val: Any) -> MissionTemplate:
    """Retrieve mission template by MissionType enum, string name, or fallback to RECONNAISSANCE."""
    if isinstance(mission_val, MissionType):
        return MISSION_TEMPLATES.get(mission_val, MISSION_TEMPLATES[MissionType.RECONNAISSANCE])
    if isinstance(mission_val, str):
        val_lower = mission_val.lower()
        for mtype, template in MISSION_TEMPLATES.items():
            if mtype.value.lower() == val_lower or mtype.name.lower() == val_lower or template.name.lower() == val_lower:
                return template
        # Fallback partial string matching
        if "recon" in val_lower or "intel" in val_lower:
            return MISSION_TEMPLATES[MissionType.RECONNAISSANCE]
        elif "border" in val_lower or "patrol" in val_lower:
            return MISSION_TEMPLATES[MissionType.BORDER_PATROL]
        elif "strike" in val_lower or "attack" in val_lower:
            return MISSION_TEMPLATES[MissionType.STRIKE_MISSION]
        elif "covert" in val_lower or "stealth" in val_lower:
            return MISSION_TEMPLATES[MissionType.COVERT_MISSION]
        elif "rescue" in val_lower or "emergency" in val_lower:
            return MISSION_TEMPLATES[MissionType.SEARCH_AND_RESCUE]
        elif "cargo" in val_lower or "transport" in val_lower:
            return MISSION_TEMPLATES[MissionType.CARGO_TRANSPORT]
        elif "intercept" in val_lower:
            return MISSION_TEMPLATES[MissionType.AIR_INTERCEPT]

    return MISSION_TEMPLATES[MissionType.RECONNAISSANCE]
