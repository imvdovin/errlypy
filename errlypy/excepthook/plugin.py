import sys
from types import TracebackType
from typing import Optional, Type

from errlypy.api import Plugin
from errlypy.exception.callback import ExceptionCallbackImpl


class ExceptHookPlugin(Plugin):
    def setup(self):
        sys.excepthook = self

    def __call__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: Optional[TracebackType],
    ):
        callback = ExceptionCallbackImpl()
        callback(exc_type, exc_value, exc_traceback)
