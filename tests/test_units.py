import pytest
from hypothesis import given
from hypothesis import strategies as st

from junction.units import (
    PCU,
    VehicleClass,
    density_vpkm,
    headway_s,
    kmh_to_ms,
    ms_to_kmh,
    pcu_flow,
    vph_to_vps,
    vps_to_vph,
)


def test_speed_conversion() -> None:
    assert kmh_to_ms(36) == pytest.approx(10)
    assert ms_to_kmh(10) == pytest.approx(36)


@given(st.floats(0, 300))
def test_speed_round_trip(v: float) -> None:
    assert ms_to_kmh(kmh_to_ms(v)) == pytest.approx(v)


@given(st.floats(0, 10_000))
def test_flow_round_trip(q: float) -> None:
    assert vps_to_vph(vph_to_vps(q)) == pytest.approx(q)


def test_headway() -> None:
    assert headway_s(1800) == 2.0


def test_density_from_flow_and_speed() -> None:
    assert density_vpkm(1500, 50) == 30


@pytest.mark.parametrize("bad", [0, -1])
def test_zero_or_negative_inputs_are_rejected(bad: float) -> None:
    with pytest.raises(ValueError):
        headway_s(bad)
    with pytest.raises(ValueError):
        density_vpkm(100, bad)


def test_every_vehicle_class_has_a_pcu() -> None:
    assert set(PCU) == set(VehicleClass)


def test_pcu_flow() -> None:
    counts = {VehicleClass.CAR: 900, VehicleClass.BUS: 20, VehicleClass.BICYCLE: 50}
    assert pcu_flow(counts) == pytest.approx(900 + 40 + 10)


def test_negative_counts_are_rejected() -> None:
    with pytest.raises(ValueError):
        pcu_flow({VehicleClass.CAR: -1})
