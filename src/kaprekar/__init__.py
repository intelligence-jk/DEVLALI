"""Kaprekar's routine for 3 and 4 digit numbers."""
from .core import (
    TARGETS,
    routine_step,
    chain,
    steps_to_fixed_point,
    histogram,
    RepdigitError,
)

__all__ = [
    "TARGETS",
    "routine_step",
    "chain",
    "steps_to_fixed_point",
    "histogram",
    "RepdigitError",
]
