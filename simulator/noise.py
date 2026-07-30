"""
Noise Module
Provides stochastic noise models (Gaussian, Rician, Rayleigh) and seed control for reproducible simulation.
"""

import random
import numpy as np
from typing import Optional, Tuple


class NoiseEngine:
    """Manages deterministic random state and stochastic noise generators."""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self._python_rng = random.Random(seed)
        self._np_rng = np.random.RandomState(seed if seed is not None else random.randint(0, 1000000))

    def reseed(self, seed: Optional[int]) -> None:
        """Reset random seeds for determinism."""
        self.seed = seed
        self._python_rng = random.Random(seed)
        self._np_rng = np.random.RandomState(seed if seed is not None else random.randint(0, 1000000))

    def gaussian_noise(self, mean: float = 0.0, std_dev: float = 0.05) -> float:
        """Generates zero-mean Gaussian noise."""
        return float(self._np_rng.normal(loc=mean, scale=std_dev))

    def rician_noise(self, v: float, sigma: float = 0.05) -> float:
        """
        Generates Rician distributed noise (ideal for envelope radar measurements with specular signal).
        v: signal amplitude, sigma: noise scale.
        """
        x = self._np_rng.normal(v, sigma)
        y = self._np_rng.normal(0, sigma)
        return float(np.sqrt(x**2 + y**2))

    def rayleigh_noise(self, scale: float = 0.05) -> float:
        """Generates Rayleigh distributed noise for fading channels."""
        return float(self._np_rng.rayleigh(scale=scale))

    def apply_noise(
        self,
        base_value: float,
        noise_level: float = 0.05,
        distribution: str = "gaussian"
    ) -> Tuple[float, float]:
        """
        Applies stochastic noise to a base value.
        Returns: (noisy_value_bounded, raw_noise_added)
        """
        if noise_level <= 0.0:
            return max(0.0, min(1.0, base_value)), 0.0

        if distribution == "rician":
            noisy_val = self.rician_noise(base_value, noise_level)
            noise_delta = noisy_val - base_value
        elif distribution == "rayleigh":
            ray_noise = self.rayleigh_noise(noise_level)
            noise_delta = ray_noise - noise_level
            noisy_val = base_value + noise_delta
        else:  # gaussian
            noise_delta = self.gaussian_noise(mean=0.0, std_dev=noise_level)
            noisy_val = base_value + noise_delta

        bounded_val = max(0.0, min(1.0, noisy_val))
        return float(bounded_val), float(noise_delta)
