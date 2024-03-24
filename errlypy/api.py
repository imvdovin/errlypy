from abc import ABC, abstractmethod
from collections import OrderedDict
from types import TracebackType
from typing import Any, Optional, Type


class ExceptionCallback(ABC):
    _next_callback: Optional["ExceptionCallback"] = None

    @abstractmethod
    def set_next(self, callback: "ExceptionCallback") -> "ExceptionCallback":
        pass

    @abstractmethod
    def __call__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: Optional[TracebackType],
    ):
        pass


class ExceptionCallbackWithContext(ExceptionCallback):
    @abstractmethod
    def set_context(self, data: dict[str, Any]) -> None:
        pass


class Extractor(ABC):
    @abstractmethod
    def extract(self, raw_data: Any) -> Any:
        pass


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
