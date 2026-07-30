"""
Multi-Target Scenario Module
Handles generation, composition, and ground-truth tracking for multi-target scenarios.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from simulator.profiles import AircraftType, AircraftProfile, get_profile
from simulator.environment import EnvironmentConfig


@dataclass
class TargetState:
    target_id: str
    aircraft_type: AircraftType
    profile: AircraftProfile
    distance_km: float
    heading_deg: float
    speed_knots: float
    altitude_m: float
    rcs_m2: float
    ir_emission: float
    thermal_delta_c: float
    acoustic_spl_db: float
    visual_contrast: float
    stealth_rating: float
    is_primary: bool = True
    threat_category: str = "CIVILIAN"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_id": self.target_id,
            "aircraft_type": self.aircraft_type.value,
            "distance_km": round(self.distance_km, 1),
            "heading_deg": round(self.heading_deg, 1),
            "speed_knots": round(self.speed_knots, 1),
            "altitude_m": round(self.altitude_m, 1),
            "rcs_m2": round(self.rcs_m2, 4),
            "stealth_rating": round(self.stealth_rating, 3),
            "is_primary": self.is_primary,
            "threat_category": self.threat_category
        }


@dataclass
class MultiTargetScenario:
    scenario_id: str
    primary_target: TargetState
    secondary_targets: List[TargetState] = field(default_factory=list)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    scenario_metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_targets(self) -> int:
        return 1 + len(self.secondary_targets)

    def get_all_targets(self) -> List[TargetState]:
        return [self.primary_target] + self.secondary_targets

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "total_targets": self.total_targets,
            "primary_target": self.primary_target.to_dict(),
            "secondary_targets": [t.to_dict() for t in self.secondary_targets],
            "metadata": self.scenario_metadata
        }
