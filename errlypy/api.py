from abc import ABC, abstractmethod
from collections import OrderedDict
from types import TracebackType
from typing import Any, List, Optional, Type

from errlypy.exception import ParsedExceptionDto


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
    ) -> ParsedExceptionDto:
        pass


class ExceptionCallbackWithContext(ExceptionCallback):
    @abstractmethod
    def set_context(self, data: ParsedExceptionDto) -> None:
        pass


class Extractor(ABC):
    @abstractmethod
    def extract(self, raw_data: Any) -> Any:
        pass


class Plugin(ABC):
    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def revert(self) -> None:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class UninitializedPluginController(ABC):
    @staticmethod
    @abstractmethod
    def init(plugins: List[Plugin]) -> "PluginController":
        pass


class PluginController(ABC):
    _registry: OrderedDict[type, Plugin]

    @abstractmethod
    def register(self, *args) -> None:
        pass

    @abstractmethod
    def revert(self) -> UninitializedPluginController:
        pass
