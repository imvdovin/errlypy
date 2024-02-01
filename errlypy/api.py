from abc import ABC, abstractmethod
from types import TracebackType
from typing import Type, Any, Optional


class ExceptionCallback(ABC):
    _next_callback: Optional["ExceptionCallback"] = None
    _dry_mode: bool = False

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
