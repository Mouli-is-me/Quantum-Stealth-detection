"""
Scenario Validation Engine Module
Enforces engineering & physics validation rules, preventing impossible scenario parameter combinations.
"""

from typing import Dict, Any, List, Tuple
from simulator.profiles import AircraftType, AircraftProfile, get_profile
from simulator.environment import EnvironmentConfig, Weather


class ScenarioValidationError(ValueError):
    """Raised when a scenario violates physical or engineering constraints."""
    pass


class ScenarioValidator:
    """Validates scenario parameters against physics & profile constraints."""

    @staticmethod
    def validate_target_physics(
        profile: AircraftProfile,
        speed_knots: float,
        altitude_m: float,
        rcs_m2: float,
        stealth_rating: float,
        acoustic_spl_db: float
    ) -> Tuple[bool, List[str]]:
        """
        Validates target physical bounds against engineering constraints.
        Returns: (is_valid, list_of_violation_messages)
        """
        violations = []

        # 1. Speed Range Check
        min_s, max_s = profile.speed_range_knots
        if speed_knots < min_s * 0.7 or speed_knots > max_s * 1.3:
            violations.append(
                f"{profile.name} speed ({speed_knots:.1f} kts) outside realistic limits [{min_s:.1f}, {max_s:.1f} kts]."
            )

        # 2. Altitude Range Check
        min_alt, max_alt = profile.altitude_range_m
        if altitude_m < min_alt * 0.5 or altitude_m > max_alt * 1.5:
            violations.append(
                f"{profile.name} altitude ({altitude_m:.1f} m) outside operational ceiling [{min_alt:.1f}, {max_alt:.1f} m]."
            )

        # 3. RCS vs Stealth Consistency Check
        if stealth_rating > 0.70 and rcs_m2 > 1.0:
            violations.append(
                f"Inconsistent stealth parameters: Stealth rating {stealth_rating:.2f} cannot have large RCS ({rcs_m2:.2f} m²)."
            )

        # 4. Impossible Hovering Check
        if profile.aircraft_type in [AircraftType.COMMERCIAL, AircraftType.CRUISE_MISSILE, AircraftType.STEALTH_FIGHTER]:
            if speed_knots < 80.0:
                violations.append(
                    f"{profile.name} cannot hover at {speed_knots:.1f} knots without aerodynamic stall."
                )

        # 5. Acoustic vs Altitude Consistency
        if profile.aircraft_type == AircraftType.BIRD and acoustic_spl_db > 60.0:
            violations.append(
                f"Biological contact (Bird) cannot produce acoustic sound pressure level of {acoustic_spl_db:.1f} dB."
            )

        is_valid = len(violations) == 0
        return is_valid, violations

    @staticmethod
    def auto_correct_target_parameters(
        profile: AircraftProfile,
        speed_knots: float,
        altitude_m: float,
        rcs_m2: float,
        stealth_rating: float,
        acoustic_spl_db: float
    ) -> Dict[str, float]:
        """
        Clamps and auto-corrects parameters to guarantee physical compliance.
        """
        # Clamp speed
        min_s, max_s = profile.speed_range_knots
        corrected_speed = max(min_s, min(max_s, speed_knots))

        # Clamp altitude
        min_alt, max_alt = profile.altitude_range_m
        corrected_alt = max(min_alt, min(max_alt, altitude_m))

        # Clamp stealth vs RCS
        min_rcs, max_rcs = profile.rcs_range_m2
        min_st, max_st = profile.stealth_rating_range
        corrected_stealth = max(min_st, min(max_st, stealth_rating))
        
        if corrected_stealth > 0.7:
            corrected_rcs = min(max_rcs, max(min_rcs, rcs_m2 * (1.0 - corrected_stealth * 0.9)))
        else:
            corrected_rcs = max(min_rcs, min(max_rcs, rcs_m2))

        # Clamp acoustic SPL
        min_spl, max_spl = profile.acoustic_spl_range_db
        corrected_spl = max(min_spl, min(max_spl, acoustic_spl_db))

        return {
            "speed_knots": corrected_speed,
            "altitude_m": corrected_alt,
            "rcs_m2": corrected_rcs,
            "stealth_rating": corrected_stealth,
            "acoustic_spl_db": corrected_spl
        }
