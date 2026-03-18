"""Global configuration for archbox."""

from dataclasses import dataclass


@dataclass
class ArchBoxConfig:
    """Global configuration."""

    default_optimizer: str = "SLSQP"
    max_iterations: int = 500
    tolerance: float = 1e-8
    backcast_method: str = "ewm"
    variance_targeting: bool = False


# Singleton global config
config = ArchBoxConfig()
