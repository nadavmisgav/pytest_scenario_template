from typing import Dict
from abc import abstractmethod, ABC


class Scenario(ABC):
    name: str
    description: str
    scenarios: Dict[str, "Scenario"] = {}

    def __init_subclass__(cls):
        Scenario.scenarios[cls.name] = cls

    @classmethod
    @abstractmethod
    def _setup(cls):
        pass

    @classmethod
    @abstractmethod
    def _teardown(cls):
        pass
