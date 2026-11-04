"""Scenario registry: `load("coding")` imports scenarios/coding.py and returns its SCENARIO."""

from importlib import import_module

from scenario import Scenario

NAMES = ("analytics", "coding", "kei_provisioning")


def load(name: str) -> Scenario:
    if name not in NAMES:
        raise ValueError(f"unknown scenario {name!r}; choose from {', '.join(NAMES)}")
    return import_module(f"scenarios.{name}").SCENARIO
