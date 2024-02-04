import sys
from typing import Type, Optional
from types import TracebackType
from errlypy.integrations.api import IntegrationPlugin
from errlypy.lib import ExceptionCallbackImpl


class ExceptHookIntegrationPlugin(IntegrationPlugin):
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
