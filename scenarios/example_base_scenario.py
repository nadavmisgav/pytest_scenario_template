from .scenario import Scenario


class BaseScenario(Scenario):
    name = "base"
    description = "Base scenario"
    attributes = {
        "a": 1,
        "b": 2,
    }

    @classmethod
    def _setup(cls):
        with open('log', "a") as fp:
            print(f"Starting scenario {cls.name=}", file=fp)

    @classmethod
    def _teardown(cls):
        with open('log', "a") as fp:
            print(f"Ending {cls.name=}\n", file=fp)
