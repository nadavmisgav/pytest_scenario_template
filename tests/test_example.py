import pytest
from scenarios import *


class TestAttributesA:
    _scenarios = [
        BaseScenario,
        AdvancedScenario
    ]

    @ pytest.mark.parametrize("attr", [1, 2, 3])
    def test_attr_a(self, scenario, attr):
        with open('log', "a") as fp:
            print(
                f"Start test_attr_a with {scenario.name=} {attr=}", file=fp)


class TestAttributesB:
    _scenarios = [
        BaseScenario,
    ]

    def test_attr_b(self, scenario):
        with open('log', "a") as fp:
            print(f"Start test_attr_b {scenario.name =}", file=fp)
