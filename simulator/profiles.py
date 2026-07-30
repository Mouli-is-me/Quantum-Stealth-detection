"""
Aircraft Profiles Module
Defines target categories and parameter bounds for physics-inspired sensor simulation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, Any


class AircraftType(Enum):
    COMMERCIAL = "Commercial Aircraft"
    STEALTH_FIGHTER = "Stealth Fighter"
    RECON_DRONE = "Recon Drone"
    CRUISE_MISSILE = "Cruise Missile"
    HELICOPTER = "Helicopter"
    BIRD = "Bird"
    UNKNOWN = "Unknown Object"


@dataclass
class AircraftProfile:
    name: str
    aircraft_type: AircraftType
    speed_range_knots: Tuple[float, float]       # Speed in knots (1 knot ≈ 0.514 m/s)
    altitude_range_m: Tuple[float, float]        # Altitude in meters
    rcs_range_m2: Tuple[float, float]            # Radar Cross Section in m²
    ir_emission_range: Tuple[float, float]       # Normalized IR radiation factor [0.0, 1.0]
    thermal_delta_range_c: Tuple[float, float]   # Thermal delta above ambient (°C)
    acoustic_spl_range_db: Tuple[float, float]   # Sound Pressure Level at 1m (dB SPL)
    visual_contrast_range: Tuple[float, float]   # Visual contrast factor [0.0, 1.0]
    stealth_rating_range: Tuple[float, float]    # Normalized stealth index [0.0, 1.0]
    max_acceleration_g: float                    # Max structural G acceleration limit
    evasive_probability: float                   # Probability of performing evasive maneuvers [0.0, 1.0]
    threat_category: str                         # Threat classification ("CIVILIAN", "MILITARY_STRIKE", "RECON", "CLUTTER")
    description: str


PROFILES: Dict[AircraftType, AircraftProfile] = {
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
        description="Large civilian airliner with high RCS, high jet engine heat, and prominent acoustic footprint."
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
        description="Unmanned aerial vehicle featuring compact RCS, low noise motor, and moderate IR emission."
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
        description="Low-altitude terrain-following missile with small frontal RCS and high speed."
    ),
    AircraftType.HELICOPTER: AircraftProfile(
        name="Helicopter",
        aircraft_type=AircraftType.HELICOPTER,
        speed_range_knots=(60.0, 170.0),
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
        description="Rotary wing aircraft with significant main rotor radar reflections and intense low-frequency acoustic noise."
    ),
    AircraftType.BIRD: AircraftProfile(
        name="Bird",
        aircraft_type=AircraftType.BIRD,
        speed_range_knots=(15.0, 45.0),
        altitude_range_m=(10.0, 600.0),
        rcs_range_m2=(0.005, 0.02),
        ir_emission_range=(0.02, 0.08),
        thermal_delta_range_c=(2.0, 8.0),
        acoustic_spl_range_db=(20.0, 45.0),
        visual_contrast_range=(0.05, 0.15),
        stealth_rating_range=(0.92, 0.99),
        max_acceleration_g=5.0,
        evasive_probability=0.85,
        threat_category="CLUTTER",
        description="Biological clutter element with minimal RCS, ambient biological temperature, and low velocity."
    ),
    AircraftType.UNKNOWN: AircraftProfile(
        name="Unknown Object",
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
        description="Unidentified contact with wide non-standard parameter ranges."
    ),
}


def get_profile(aircraft_type_val: Any) -> AircraftProfile:
    """Retrieve aircraft profile by AircraftType enum, string name, or fallback to UNKNOWN."""
    if isinstance(aircraft_type_val, AircraftType):
        return PROFILES.get(aircraft_type_val, PROFILES[AircraftType.UNKNOWN])
    
    if isinstance(aircraft_type_val, str):
        for atype, profile in PROFILES.items():
            if atype.value.lower() == aircraft_type_val.lower() or atype.name.lower() == aircraft_type_val.lower():
                return profile
                
    return PROFILES[AircraftType.UNKNOWN]
