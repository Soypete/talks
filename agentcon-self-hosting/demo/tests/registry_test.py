import pytest

from scenarios import load


def test_analytics_scenario_loads_and_is_well_formed():
    s = load("analytics")
    names = {t["function"]["name"] for t in s.tools}
    assert s.terminal_tool in names
    assert set(s.required_steps) <= names
    assert all(p["tool"] in names and p["requires"] in names for p in s.prerequisites)


def test_unknown_scenario_is_rejected():
    with pytest.raises(ValueError, match="unknown scenario"):
        load("nope")
