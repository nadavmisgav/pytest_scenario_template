from dataclasses import dataclass, field
import pytest
import re
from typing import Callable, DefaultDict, Dict, List

from scenarios import Scenario


@dataclass
class TestSuite:
    """
    Class to describe a suite of tests
    """
    setup: Callable = None
    tests: List[Callable] = field(default_factory=list)
    teardown: Callable = None


def pytest_addoption(parser):
    """
    Hook the addoption to add the scenario and no-setup
    options
    """
    parser.addoption(
        "--scenarios",
        nargs='*',
        metavar="scenario",
        choices=Scenario.scenarios.keys(),
        help="scenarios to run, leave empty to print scenarios",
    )

    parser.addoption(
        "--no-setup",
        action="store_true",
        help="Disable setup and teardown",
        default=False
    )


def pytest_cmdline_main(config):
    """
    Hook the cmdline main to check if test should be run
    or only list available scenarios
    """
    try:
        if len(config.option.scenarios) == 0:
            print("Available scenarios:")
            for scenario in Scenario.scenarios.values():
                print(f"  {scenario.name} - {scenario.description}")
            return 0
    except:
        pass

    return None


def pytest_generate_tests(metafunc):
    """
    Hook pytest test generation to parametrize the tests
    to each scenario they are supposed to be included in and to generate
    the setup and teardown tests for each scenario.
    """

    # test is setup or teardown - parametrize to all scenarios
    if metafunc.function.__name__ in ["test_setup", "test_teardown"]:
        metafunc.parametrize(
            "scenario", Scenario.scenarios.values())

    # parameterize test for each scenario it is included in
    else:
        metafunc.parametrize(
            "scenario",  metafunc.cls._scenarios)


def should_skip_scenario(scenario, config_scenarios):
    """
    Checks if the scenario parametrized to test should be filtered
    by what is set in config_scenarios
    """
    for config_scenario in config_scenarios:
        if scenario == Scenario.scenarios[config_scenario].__name__:
            return False

    return True


# match scenario from test name e.g,
# test_attr_a[AdvancedScenario-1]
#             ^^^^^^^^^^^^^^^^
scenario_re = re.compile(r".*\[(\w*).*\].*")


def pytest_collection_modifyitems(session, config, items):
    """
    Hook collection modification to order tests by scenario, each
    scenario will start with it's setup, preceding with the tests and
    finally the teardown.
    """

    test_scenarios = DefaultDict(TestSuite)

    config_scenarios = config.option.scenarios
    filter_scenarios = config_scenarios is not None
    skip_setup = config.option.no_setup

    if skip_setup and (not filter_scenarios or len(config_scenarios) > 1):
        raise RuntimeWarning(
            "Configured no setup and teardown but more then one scenario is configured")

    # Group tests by scenario in to TestSuite objects
    for test in items:
        scenario = scenario_re.match(test.name).groups()[0]

        if filter_scenarios and should_skip_scenario(scenario, config_scenarios):
            continue

        if test.originalname == "test_setup":
            test_scenarios[scenario].setup = test
        elif test.originalname == "test_teardown":
            test_scenarios[scenario].teardown = test
        else:
            test_scenarios[scenario].tests.append(test)

    # Clear all pytest tests
    items.clear()

    # Order tests
    for scenario in test_scenarios.values():
        if len(scenario.tests) != 0:
            suite = scenario.tests
            if not skip_setup:
                suite.insert(0, scenario.setup)
                suite.append(scenario.teardown)

            items.extend(suite)


_scenario_setup_failed: Dict[str, bool] = {}


def pytest_runtest_makereport(item, call):
    """
    Hook makereport to mark if the scenario setup has failed
    """
    if item.originalname == "test_setup" and call.when == "call":
        try:
            # TODO: not sure if this check is enough
            failed = not call.result == []
        except:
            # call does not have valid result attribute if some exception happended
            # during the test
            failed = True

        scenario = scenario_re.match(item.name).groups()[0]
        _scenario_setup_failed[scenario] = failed


def pytest_runtest_setup(item):
    """
    Hook runtest_setup to skip test if their scenario setup has failed
    """
    if not item.originalname == "test_setup":
        scenario = scenario_re.match(item.name).groups()[0]
        if _scenario_setup_failed[scenario]:
            pytest.skip(f"Setup for {scenario} failed, skipping...")
