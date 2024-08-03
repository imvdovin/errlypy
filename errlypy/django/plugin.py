from types import TracebackType
from typing import Any, Type, Tuple

from django.core.handlers import exception

from errlypy.api import Plugin
from errlypy.internal.event import EventTypeFactory
from errlypy.internal.observable import Observable
from errlypy.django.events import OnDjangoExceptionHasBeenParsedEvent
from errlypy.exception.callback import ExceptionCallbackImpl


class DjangoExceptionPlugin(Plugin, Observable):
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
        exc_info: Tuple[Type[BaseException], BaseException, TracebackType],
    ) -> Any:
        response = self._callback(exc_info[0], exc_info[1], exc_info[2])

        self.notify(
            EventTypeFactory.get(OnDjangoExceptionHasBeenParsedEvent),
            response,
        )

        return self._original_fn(request, resolver, exc_info)
