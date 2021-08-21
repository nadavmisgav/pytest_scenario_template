# Pytest Scenarios

Template for pytest to run scenarios, each class will run in context of all the scenarios that are configured for it.  
All scenarios have a generic `test_setup` and `test_teardown` for configuring the scenario.

> If the setup fails all tests in the scenario will be skipped.

## Scenarios

Each scenario will be defined in the `scenarios` folder and must be derived from the `Scenario` base class. A scenario must implement a `_setup` and `_teardown` methods. Futhermore it must have the following attributes,

```python
name: str # Scenario name will be used to reference scenarios to run.
description: str # Scenario description will be used to describe the scenario in help messages
```

> Any other attribute can be optionally inserted to be used in tests

Example:

```python
class BaseScenario(Scenario):
    name = "base"
    description = "Base scenario"
    attributes = {
        "a": 1,
        "b": 2,
    }

    @classmethod
    def _setup(cls):
        pass

    @classmethod
    def _teardown(cls):
        pass
```

> Remember to add it to `__init__.py`

## Creating tests

> Supports only test classes

### Class

Each test class _must_ include a `_scenarios` attribute that is a list of `Scenario` objects that the tests are to be included in.
Example:

```python
class TestFoo:
    _scenarios = [
        BaseScenario,
    ]
    pass
```

### Test functions

Each test function must accept as its _first parameter_ a `scenario` that will include all the data in the `Scenario` class.
Example:

```python
def test_foo(self, scenario):
    pass
```

## Usage

Scenario adds the following command line options,

### [Optional] scenarios

By default all scenarios are tests, this allows the user to filter which scenarios to run based on their names,

> If none are given prints the available scenarios

```
# pytest --scenarios base advanced
...

# pytest --scenarios
Available scenarios:
  base - Base scenario
  advanced - Advanced scenario
  stress - Stress scenario
```

### [Optional] no-setup

Disables the setup and teardown methods from each scenario

```
# pytest --no-setup --scenarios base
```

> Must filter only one scenario when used!

## Example

See the [example](https://github.com/nadavmisgav/pytest_scenario_template/tree/example) branch.
