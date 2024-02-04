from abc import ABC, abstractmethod
from collections import OrderedDict


class IntegrationPlugin(ABC):
    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def revert(self) -> None:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class Integration(ABC):
    _registry: OrderedDict[type, IntegrationPlugin]
    _has_setup_been_called: bool

    @abstractmethod
    def register(self, *args) -> None:
        pass

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def revert(self) -> None:
        pass
