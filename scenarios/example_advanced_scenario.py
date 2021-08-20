from .scenario import Scenario


class AdvancedScenario(Scenario):
    name = "advanced"
    description = "Advanced scenario"
    attributes = {
        "a": 4,
        "b": 8,
    }

    @classmethod
    def _setup(cls):
        with open('log', "a") as fp:
            print(f"Starting scenario {cls.name=}", file=fp)

    @classmethod
    def _teardown(cls):
        with open('log', "a") as fp:
            print(f"Ending {cls.name=}\n", file=fp)
