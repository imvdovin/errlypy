from typing import Any
from types import TracebackType
from django.core.handlers import exception
from errlypy.lib import ExceptionCallbackImpl
from errlypy.integrations.api import IntegrationPlugin


class DjangoIntegrationPlugin(IntegrationPlugin):
    def setup(self):
        self._callback = ExceptionCallbackImpl.create()
        self._original_fn = exception.handle_uncaught_exception
        exception.handle_uncaught_exception = self

    def revert(self):
        exception.handle_uncaught_exception = self._original_fn

    def __call__(
        self,
        request,
        resolver,
        exc_info: tuple[type[BaseException], BaseException, TracebackType],
    ) -> Any:
        self._callback(exc_info[0], exc_info[1], exc_info[2])

        return self._original_fn(request, resolver, exc_info)
