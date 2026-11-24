"""Traffic units: speeds, flows, densities and passenger car units.

The simulator works in metres, seconds and vehicles. Input files and reports use the units
traffic engineers read: km/h, vehicles per hour and vehicles per kilometre.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum


class VehicleClass(StrEnum):
    CAR = "car"
    VAN = "van"
    BUS = "bus"
    HGV = "hgv"
    MOTORCYCLE = "motorcycle"
    BICYCLE = "bicycle"


PCU: dict[VehicleClass, float] = {
    VehicleClass.CAR: 1.0,
    VehicleClass.VAN: 1.0,
    VehicleClass.BUS: 2.0,
    VehicleClass.HGV: 2.3,
    VehicleClass.MOTORCYCLE: 0.4,
    VehicleClass.BICYCLE: 0.2,
}
"""Passenger car unit equivalents at signalised junctions (UK practice)."""


def kmh_to_ms(speed_kmh: float) -> float:
    return speed_kmh / 3.6


def ms_to_kmh(speed_ms: float) -> float:
    return speed_ms * 3.6


def vph_to_vps(flow_vph: float) -> float:
    """Vehicles per hour to vehicles per second."""
    return flow_vph / 3600.0


def vps_to_vph(flow_vps: float) -> float:
    return flow_vps * 3600.0


def headway_s(flow_vph: float) -> float:
    """Average time gap between vehicles for a flow."""
    if flow_vph <= 0:
        raise ValueError("flow must be positive")
    return 3600.0 / flow_vph


def density_vpkm(flow_vph: float, speed_kmh: float) -> float:
    """Density from the fundamental relation q = k v."""
    if speed_kmh <= 0:
        raise ValueError("speed must be positive")
    return flow_vph / speed_kmh


def pcu_flow(counts_vph: Mapping[VehicleClass, float]) -> float:
    """Convert a classified count to passenger car units per hour."""
    if any(v < 0 for v in counts_vph.values()):
        raise ValueError("counts cannot be negative")
    return sum(PCU[cls] * v for cls, v in counts_vph.items())
