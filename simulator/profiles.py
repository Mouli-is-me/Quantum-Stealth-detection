"""
Aircraft Profiles Module
Defines expanded target categories and physics parameter bounds for sensor simulation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, Any


class AircraftType(Enum):
    # 19 Expanded Aircraft / Target Types
    BIRD = "Bird"
    BIRD_FLOCK = "Bird Flock"
    CIVILIAN_DRONE = "Civilian Drone"
    RECON_DRONE = "Recon Drone"
    MILITARY_UAV = "Military UAV"
    COMBAT_UAV = "Combat UAV"
    QUADCOPTER = "Quadcopter"
    CARGO_DRONE = "Cargo Drone"
    HELICOPTER = "Helicopter"
    ATTACK_HELICOPTER = "Attack Helicopter"
    COMMERCIAL = "Commercial Aircraft"
    PASSENGER_AIRCRAFT = "Passenger Aircraft"
    CARGO_AIRCRAFT = "Cargo Aircraft"
    BUSINESS_JET = "Business Jet"
    FIGHTER_JET = "Fighter Jet"
    STEALTH_FIGHTER = "Stealth Fighter"
    BOMBER = "Bomber"
    CRUISE_MISSILE = "Cruise Missile"
    UNKNOWN = "Unknown Aircraft"


@dataclass
class AircraftProfile:
    name: str
    aircraft_type: AircraftType
    speed_range_knots: Tuple[float, float]       # Speed in knots
    altitude_range_m: Tuple[float, float]        # Altitude in meters
    rcs_range_m2: Tuple[float, float]            # Radar Cross Section in m²
    ir_emission_range: Tuple[float, float]       # Normalized IR factor [0.0, 1.0]
    thermal_delta_range_c: Tuple[float, float]   # Thermal delta above ambient (°C)
    acoustic_spl_range_db: Tuple[float, float]   # Sound Pressure Level at 1m (dB SPL)
    visual_contrast_range: Tuple[float, float]   # Visual contrast factor [0.0, 1.0]
    stealth_rating_range: Tuple[float, float]    # Normalized stealth index [0.0, 1.0]
    max_acceleration_g: float                    # Max structural G limit
    evasive_probability: float                   # Probability of evasive maneuvers
    threat_category: str                         # Threat classification ("CIVILIAN", "MILITARY_STRIKE", "RECON", "CLUTTER", "UNKNOWN")
    description: str


PROFILES: Dict[AircraftType, AircraftProfile] = {
    AircraftType.BIRD: AircraftProfile(
        name="Bird",
        aircraft_type=AircraftType.BIRD,
        speed_range_knots=(10.0, 35.0),
        altitude_range_m=(10.0, 400.0),
        rcs_range_m2=(0.002, 0.015),
        ir_emission_range=(0.01, 0.06),
        thermal_delta_range_c=(1.0, 5.0),
        acoustic_spl_range_db=(15.0, 35.0),
        visual_contrast_range=(0.05, 0.12),
        stealth_rating_range=(0.94, 0.99),
        max_acceleration_g=4.0,
        evasive_probability=0.85,
        threat_category="CLUTTER",
        description="Single avian target with negligible RCS and biological thermal signature."
    ),
    AircraftType.BIRD_FLOCK: AircraftProfile(
        name="Bird Flock",
        aircraft_type=AircraftType.BIRD_FLOCK,
        speed_range_knots=(15.0, 45.0),
        altitude_range_m=(50.0, 1200.0),
        rcs_range_m2=(0.05, 0.40),
        ir_emission_range=(0.03, 0.12),
        thermal_delta_range_c=(2.0, 8.0),
        acoustic_spl_range_db=(30.0, 55.0),
        visual_contrast_range=(0.15, 0.35),
        stealth_rating_range=(0.75, 0.90),
        max_acceleration_g=3.0,
        evasive_probability=0.90,
        threat_category="CLUTTER",
        description="Migratory bird swarm creating distributed radar clutter signature."
    ),
    AircraftType.CIVILIAN_DRONE: AircraftProfile(
        name="Civilian Drone",
        aircraft_type=AircraftType.CIVILIAN_DRONE,
        speed_range_knots=(10.0, 40.0),
        altitude_range_m=(20.0, 300.0),
        rcs_range_m2=(0.01, 0.08),
        ir_emission_range=(0.05, 0.18),
        thermal_delta_range_c=(5.0, 15.0),
        acoustic_spl_range_db=(50.0, 70.0),
        visual_contrast_range=(0.3, 0.5),
        stealth_rating_range=(0.70, 0.88),
        max_acceleration_g=3.0,
        evasive_probability=0.20,
        threat_category="CIVILIAN",
        description="Small recreational drone operating at low altitude."
    ),
    AircraftType.QUADCOPTER: AircraftProfile(
        name="Quadcopter",
        aircraft_type=AircraftType.QUADCOPTER,
        speed_range_knots=(15.0, 50.0),
        altitude_range_m=(10.0, 500.0),
        rcs_range_m2=(0.01, 0.05),
        ir_emission_range=(0.04, 0.15),
        thermal_delta_range_c=(4.0, 12.0),
        acoustic_spl_range_db=(55.0, 75.0),
        visual_contrast_range=(0.25, 0.45),
        stealth_rating_range=(0.75, 0.90),
        max_acceleration_g=4.5,
        evasive_probability=0.35,
        threat_category="CIVILIAN",
        description="Agile multi-rotor quadcopter with low acoustic signature."
    ),
    AircraftType.CARGO_DRONE: AircraftProfile(
        name="Cargo Drone",
        aircraft_type=AircraftType.CARGO_DRONE,
        speed_range_knots=(40.0, 90.0),
        altitude_range_m=(100.0, 1500.0),
        rcs_range_m2=(0.2, 0.8),
        ir_emission_range=(0.15, 0.35),
        thermal_delta_range_c=(12.0, 25.0),
        acoustic_spl_range_db=(70.0, 85.0),
        visual_contrast_range=(0.4, 0.6),
        stealth_rating_range=(0.45, 0.65),
        max_acceleration_g=2.5,
        evasive_probability=0.10,
        threat_category="CIVILIAN",
        description="Autonomous logistics delivery drone."
    ),
    AircraftType.RECON_DRONE: AircraftProfile(
        name="Recon Drone",
        aircraft_type=AircraftType.RECON_DRONE,
        speed_range_knots=(100.0, 220.0),
        altitude_range_m=(2000.0, 8000.0),
        rcs_range_m2=(0.1, 0.8),
        ir_emission_range=(0.2, 0.45),
        thermal_delta_range_c=(15.0, 30.0),
        acoustic_spl_range_db=(70.0, 85.0),
        visual_contrast_range=(0.35, 0.5),
        stealth_rating_range=(0.5, 0.75),
        max_acceleration_g=4.0,
        evasive_probability=0.30,
        threat_category="RECON",
        description="Unmanned ISR platform with moderate stealth and long loiter duration."
    ),
    AircraftType.MILITARY_UAV: AircraftProfile(
        name="Military UAV",
        aircraft_type=AircraftType.MILITARY_UAV,
        speed_range_knots=(120.0, 280.0),
        altitude_range_m=(3000.0, 10000.0),
        rcs_range_m2=(0.15, 1.2),
        ir_emission_range=(0.25, 0.50),
        thermal_delta_range_c=(18.0, 35.0),
        acoustic_spl_range_db=(75.0, 90.0),
        visual_contrast_range=(0.35, 0.55),
        stealth_rating_range=(0.45, 0.70),
        max_acceleration_g=4.5,
        evasive_probability=0.40,
        threat_category="RECON",
        description="Medium-altitude long-endurance tactical military UAV."
    ),
    AircraftType.COMBAT_UAV: AircraftProfile(
        name="Combat UAV",
        aircraft_type=AircraftType.COMBAT_UAV,
        speed_range_knots=(250.0, 500.0),
        altitude_range_m=(3000.0, 12000.0),
        rcs_range_m2=(0.02, 0.20),
        ir_emission_range=(0.20, 0.40),
        thermal_delta_range_c=(20.0, 40.0),
        acoustic_spl_range_db=(80.0, 100.0),
        visual_contrast_range=(0.30, 0.45),
        stealth_rating_range=(0.70, 0.88),
        max_acceleration_g=7.0,
        evasive_probability=0.60,
        threat_category="MILITARY_STRIKE",
        description="Low-observable unmanned strike platform engineered for deep penetration."
    ),
    AircraftType.HELICOPTER: AircraftProfile(
        name="Helicopter",
        aircraft_type=AircraftType.HELICOPTER,
        speed_range_knots=(60.0, 160.0),
        altitude_range_m=(50.0, 1500.0),
        rcs_range_m2=(3.0, 8.0),
        ir_emission_range=(0.6, 0.85),
        thermal_delta_range_c=(30.0, 50.0),
        acoustic_spl_range_db=(115.0, 135.0),
        visual_contrast_range=(0.7, 0.85),
        stealth_rating_range=(0.05, 0.25),
        max_acceleration_g=3.5,
        evasive_probability=0.40,
        threat_category="MILITARY_STRIKE",
        description="Rotary wing aircraft with significant main rotor radar reflections and intense acoustic signature."
    ),
    AircraftType.ATTACK_HELICOPTER: AircraftProfile(
        name="Attack Helicopter",
        aircraft_type=AircraftType.ATTACK_HELICOPTER,
        speed_range_knots=(80.0, 180.0),
        altitude_range_m=(30.0, 2000.0),
        rcs_range_m2=(1.5, 4.5),
        ir_emission_range=(0.4, 0.70),
        thermal_delta_range_c=(25.0, 45.0),
        acoustic_spl_range_db=(110.0, 130.0),
        visual_contrast_range=(0.5, 0.75),
        stealth_rating_range=(0.25, 0.50),
        max_acceleration_g=4.5,
        evasive_probability=0.65,
        threat_category="MILITARY_STRIKE",
        description="Armored attack helicopter equipped with infrared suppressors."
    ),
    AircraftType.COMMERCIAL: AircraftProfile(
        name="Commercial Aircraft",
        aircraft_type=AircraftType.COMMERCIAL,
        speed_range_knots=(400.0, 550.0),
        altitude_range_m=(8000.0, 12000.0),
        rcs_range_m2=(15.0, 40.0),
        ir_emission_range=(0.75, 0.95),
        thermal_delta_range_c=(35.0, 55.0),
        acoustic_spl_range_db=(115.0, 130.0),
        visual_contrast_range=(0.8, 0.95),
        stealth_rating_range=(0.0, 0.1),
        max_acceleration_g=2.5,
        evasive_probability=0.01,
        threat_category="CIVILIAN",
        description="Large airliner with high RCS, heavy jet exhaust, and acoustic signature."
    ),
    AircraftType.PASSENGER_AIRCRAFT: AircraftProfile(
        name="Passenger Aircraft",
        aircraft_type=AircraftType.PASSENGER_AIRCRAFT,
        speed_range_knots=(420.0, 540.0),
        altitude_range_m=(8500.0, 12500.0),
        rcs_range_m2=(18.0, 45.0),
        ir_emission_range=(0.75, 0.95),
        thermal_delta_range_c=(35.0, 55.0),
        acoustic_spl_range_db=(115.0, 128.0),
        visual_contrast_range=(0.8, 0.95),
        stealth_rating_range=(0.0, 0.08),
        max_acceleration_g=2.2,
        evasive_probability=0.01,
        threat_category="CIVILIAN",
        description="Commercial passenger jet on designated airway."
    ),
    AircraftType.CARGO_AIRCRAFT: AircraftProfile(
        name="Cargo Aircraft",
        aircraft_type=AircraftType.CARGO_AIRCRAFT,
        speed_range_knots=(380.0, 500.0),
        altitude_range_m=(7000.0, 11000.0),
        rcs_range_m2=(25.0, 60.0),
        ir_emission_range=(0.80, 0.98),
        thermal_delta_range_c=(40.0, 60.0),
        acoustic_spl_range_db=(120.0, 135.0),
        visual_contrast_range=(0.85, 0.98),
        stealth_rating_range=(0.0, 0.05),
        max_acceleration_g=2.0,
        evasive_probability=0.01,
        threat_category="CIVILIAN",
        description="Heavy strategic air transport with vast radar cross section."
    ),
    AircraftType.BUSINESS_JET: AircraftProfile(
        name="Business Jet",
        aircraft_type=AircraftType.BUSINESS_JET,
        speed_range_knots=(420.0, 580.0),
        altitude_range_m=(9000.0, 14000.0),
        rcs_range_m2=(4.0, 12.0),
        ir_emission_range=(0.60, 0.82),
        thermal_delta_range_c=(30.0, 48.0),
        acoustic_spl_range_db=(105.0, 120.0),
        visual_contrast_range=(0.70, 0.88),
        stealth_rating_range=(0.10, 0.25),
        max_acceleration_g=3.0,
        evasive_probability=0.05,
        threat_category="CIVILIAN",
        description="High-altitude executive jet transport."
    ),
    AircraftType.FIGHTER_JET: AircraftProfile(
        name="Fighter Jet",
        aircraft_type=AircraftType.FIGHTER_JET,
        speed_range_knots=(500.0, 1100.0),
        altitude_range_m=(3000.0, 14000.0),
        rcs_range_m2=(1.0, 4.0),
        ir_emission_range=(0.70, 0.95),
        thermal_delta_range_c=(40.0, 75.0),
        acoustic_spl_range_db=(125.0, 145.0),
        visual_contrast_range=(0.5, 0.75),
        stealth_rating_range=(0.2, 0.45),
        max_acceleration_g=9.0,
        evasive_probability=0.70,
        threat_category="MILITARY_STRIKE",
        description="4th generation tactical air superiority fighter jet."
    ),
    AircraftType.STEALTH_FIGHTER: AircraftProfile(
        name="Stealth Fighter",
        aircraft_type=AircraftType.STEALTH_FIGHTER,
        speed_range_knots=(500.0, 1200.0),
        altitude_range_m=(5000.0, 15000.0),
        rcs_range_m2=(0.0001, 0.005),
        ir_emission_range=(0.15, 0.35),
        thermal_delta_range_c=(12.0, 25.0),
        acoustic_spl_range_db=(90.0, 110.0),
        visual_contrast_range=(0.25, 0.4),
        stealth_rating_range=(0.85, 0.98),
        max_acceleration_g=9.0,
        evasive_probability=0.75,
        threat_category="MILITARY_STRIKE",
        description="5th gen stealth aircraft utilizing Radar Absorbent Material (RAM) and engine heat masking."
    ),
    AircraftType.BOMBER: AircraftProfile(
        name="Bomber",
        aircraft_type=AircraftType.BOMBER,
        speed_range_knots=(450.0, 700.0),
        altitude_range_m=(6000.0, 15000.0),
        rcs_range_m2=(0.05, 15.0),
        ir_emission_range=(0.50, 0.85),
        thermal_delta_range_c=(30.0, 60.0),
        acoustic_spl_range_db=(115.0, 138.0),
        visual_contrast_range=(0.60, 0.85),
        stealth_rating_range=(0.30, 0.85),
        max_acceleration_g=4.0,
        evasive_probability=0.30,
        threat_category="MILITARY_STRIKE",
        description="Strategic long-range heavy strike bomber."
    ),
    AircraftType.CRUISE_MISSILE: AircraftProfile(
        name="Cruise Missile",
        aircraft_type=AircraftType.CRUISE_MISSILE,
        speed_range_knots=(450.0, 650.0),
        altitude_range_m=(30.0, 250.0),
        rcs_range_m2=(0.05, 0.25),
        ir_emission_range=(0.4, 0.65),
        thermal_delta_range_c=(25.0, 45.0),
        acoustic_spl_range_db=(95.0, 110.0),
        visual_contrast_range=(0.2, 0.35),
        stealth_rating_range=(0.6, 0.8),
        max_acceleration_g=12.0,
        evasive_probability=0.10,
        threat_category="MILITARY_STRIKE",
        description="Low-altitude terrain-following precision missile."
    ),
    AircraftType.UNKNOWN: AircraftProfile(
        name="Unknown Aircraft",
        aircraft_type=AircraftType.UNKNOWN,
        speed_range_knots=(50.0, 800.0),
        altitude_range_m=(100.0, 10000.0),
        rcs_range_m2=(0.01, 10.0),
        ir_emission_range=(0.1, 0.9),
        thermal_delta_range_c=(5.0, 40.0),
        acoustic_spl_range_db=(50.0, 110.0),
        visual_contrast_range=(0.2, 0.8),
        stealth_rating_range=(0.2, 0.8),
        max_acceleration_g=6.0,
        evasive_probability=0.50,
        threat_category="UNKNOWN",
        description="Unidentified aerial contact with unknown flight envelope."
    ),
}


def get_profile(aircraft_type_val: Any) -> AircraftProfile:
    """Retrieve aircraft profile by AircraftType enum, string name, or fallback to UNKNOWN."""
    if isinstance(aircraft_type_val, AircraftType):
        return PROFILES.get(aircraft_type_val, PROFILES[AircraftType.UNKNOWN])
    
    if isinstance(aircraft_type_val, str):
        val_lower = aircraft_type_val.lower()
        for atype, profile in PROFILES.items():
            if atype.value.lower() == val_lower or atype.name.lower() == val_lower or profile.name.lower() == val_lower:
                return profile
        # Partial match fallbacks
        if "bird" in val_lower:
            return PROFILES[AircraftType.BIRD_FLOCK] if "flock" in val_lower else PROFILES[AircraftType.BIRD]
        elif "stealth" in val_lower or "f-35" in val_lower or "f-22" in val_lower:
            return PROFILES[AircraftType.STEALTH_FIGHTER]
        elif "fighter" in val_lower:
            return PROFILES[AircraftType.FIGHTER_JET]
        elif "commercial" in val_lower or "airliner" in val_lower or "passenger" in val_lower:
            return PROFILES[AircraftType.COMMERCIAL]
        elif "drone" in val_lower or "uav" in val_lower:
            if "combat" in val_lower:
                return PROFILES[AircraftType.COMBAT_UAV]
            elif "recon" in val_lower:
                return PROFILES[AircraftType.RECON_DRONE]
            elif "quad" in val_lower:
                return PROFILES[AircraftType.QUADCOPTER]
            return PROFILES[AircraftType.MILITARY_UAV]
        elif "helicopter" in val_lower or "chopper" in val_lower:
            return PROFILES[AircraftType.ATTACK_HELICOPTER] if "attack" in val_lower else PROFILES[AircraftType.HELICOPTER]
        elif "missile" in val_lower:
            return PROFILES[AircraftType.CRUISE_MISSILE]
        elif "bomber" in val_lower:
            return PROFILES[AircraftType.BOMBER]
                
    return PROFILES[AircraftType.UNKNOWN]
