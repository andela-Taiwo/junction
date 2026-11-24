"""Fixed-time signal timing by Webster's method.

These are the textbook formulas (Webster, 1958) for an isolated junction. They give the
baseline that the adaptive controller must beat, and a closed-form check for the simulator
at low and moderate demand.

Flows are vehicles per hour; times are seconds.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def flow_ratio(flow_vph: float, saturation_flow_vph: float) -> float:
    """Return a movement's flow ratio y = q / s."""
    if flow_vph < 0:
        raise ValueError("flow cannot be negative")
    if saturation_flow_vph <= 0:
        raise ValueError("saturation flow must be positive")
    return flow_vph / saturation_flow_vph


def _total(flow_ratios: Sequence[float]) -> float:
    if not flow_ratios:
        raise ValueError("a junction needs at least one phase")
    if any(y < 0 for y in flow_ratios):
        raise ValueError("flow ratios cannot be negative")
    total = math.fsum(flow_ratios)
    if total >= 1.0:
        raise ValueError(f"junction is oversaturated: sum of critical flow ratios is {total:.3f}")
    return total


def webster_cycle(lost_time_s: float, flow_ratios: Sequence[float]) -> float:
    """Return Webster's optimum cycle length, C0 = (1.5 L + 5) / (1 - Y).

    ``flow_ratios`` holds the critical flow ratio of each phase.
    """
    if lost_time_s < 0:
        raise ValueError("lost time cannot be negative")
    return (1.5 * lost_time_s + 5.0) / (1.0 - _total(flow_ratios))


def green_splits(cycle_s: float, lost_time_s: float, flow_ratios: Sequence[float]) -> list[float]:
    """Split the effective green time between phases in proportion to their flow ratios."""
    total = _total(flow_ratios)
    effective = cycle_s - lost_time_s
    if effective <= 0:
        raise ValueError("cycle must be longer than the lost time")
    if total == 0:
        return [effective / len(flow_ratios)] * len(flow_ratios)
    return [effective * y / total for y in flow_ratios]


def webster_delay(
    cycle_s: float, green_s: float, flow_vph: float, saturation_flow_vph: float
) -> float:
    """Return Webster's average delay per vehicle, in seconds, for one movement.

    Valid for undersaturated movements (degree of saturation below 1).
    """
    if not 0 < green_s <= cycle_s:
        raise ValueError("green must be positive and no longer than the cycle")
    if flow_vph <= 0:
        raise ValueError("flow must be positive")
    lam = green_s / cycle_s
    q = flow_vph / 3600.0
    s = saturation_flow_vph / 3600.0
    if s <= 0:
        raise ValueError("saturation flow must be positive")
    x = q / (lam * s)
    if x >= 1.0:
        raise ValueError(f"movement is oversaturated: degree of saturation {x:.3f}")
    uniform = cycle_s * (1.0 - lam) ** 2 / (2.0 * (1.0 - lam * x))
    random = x * x / (2.0 * q * (1.0 - x))
    correction = 0.65 * math.pow(cycle_s / (q * q), 1.0 / 3.0) * math.pow(x, 2.0 + 5.0 * lam)
    return uniform + random - correction
