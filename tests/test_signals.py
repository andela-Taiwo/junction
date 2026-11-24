import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from junction.signals import flow_ratio, green_splits, webster_cycle, webster_delay


def test_flow_ratio() -> None:
    assert flow_ratio(450, 1800) == 0.25


@pytest.mark.parametrize(("q", "s"), [(-1, 1800), (100, 0)])
def test_flow_ratio_rejects_bad_input(q: float, s: float) -> None:
    with pytest.raises(ValueError):
        flow_ratio(q, s)


def test_webster_cycle_by_hand() -> None:
    # L = 12 s, Y = 0.6 -> (18 + 5) / 0.4
    assert webster_cycle(12, [0.35, 0.25]) == pytest.approx(57.5)


def test_oversaturated_junction_is_rejected() -> None:
    with pytest.raises(ValueError, match="oversaturated"):
        webster_cycle(12, [0.6, 0.45])


def test_no_phases_is_rejected() -> None:
    with pytest.raises(ValueError):
        webster_cycle(12, [])


def test_cycle_grows_with_demand() -> None:
    assert webster_cycle(12, [0.3, 0.3]) > webster_cycle(12, [0.2, 0.2])


def test_green_splits_by_hand() -> None:
    assert green_splits(57.5, 12, [0.35, 0.25]) == pytest.approx([26.541667, 18.958333])


@given(st.lists(st.floats(0.01, 0.2), min_size=1, max_size=4), st.floats(0, 20))
def test_green_splits_use_all_effective_green(ratios: list[float], lost: float) -> None:
    cycle = webster_cycle(lost, ratios)
    splits = green_splits(cycle, lost, ratios)
    assert math.fsum(splits) == pytest.approx(cycle - lost)
    assert all(g > 0 for g in splits)


def test_green_splits_reject_cycle_shorter_than_lost_time() -> None:
    with pytest.raises(ValueError):
        green_splits(10, 12, [0.3])


def test_webster_delay_by_hand() -> None:
    # C = 60, g = 30, s = 1800 veh/h, q = 600 veh/h -> x = 2/3
    # 11.25 (uniform) + 4.0 (random) - 1.3555 (correction)
    assert webster_delay(60, 30, 600, 1800) == pytest.approx(13.894, abs=1e-3)


def test_delay_rises_with_flow() -> None:
    delays = [webster_delay(60, 30, q, 1800) for q in (200, 400, 600, 800)]
    assert delays == sorted(delays)


def test_delay_falls_with_more_green() -> None:
    assert webster_delay(60, 40, 600, 1800) < webster_delay(60, 30, 600, 1800)


def test_oversaturated_movement_is_rejected() -> None:
    with pytest.raises(ValueError, match="oversaturated"):
        webster_delay(60, 30, 900, 1800)


@pytest.mark.parametrize(("c", "g"), [(60, 0), (60, 61)])
def test_bad_green_is_rejected(c: float, g: float) -> None:
    with pytest.raises(ValueError):
        webster_delay(c, g, 100, 1800)
