"""
This test file is a hack to create tests that will be used
as a setup and teardown for each scenario that will be tested.
"""
from .scenario import Scenario


class TestScenario:
    def test_setup(self, scenario: Scenario):
        scenario._setup()

    def test_teardown(self, scenario: Scenario):
        scenario._teardown()
