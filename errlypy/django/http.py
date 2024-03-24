from types import TracebackType
from typing import Any, Optional, Type

import aiohttp
from asgiref.sync import async_to_sync

from errlypy.api import ExceptionCallbackWithContext
from errlypy.exception.callback import BaseExceptionCallbackImpl


@async_to_sync
async def send(url: str, headers, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        session.post(url, json=data)


# FIXME: Problem - cannot validate connection (it's valid or not) on init state, not in runtime
class DjangoHTTPCallbackImpl(ExceptionCallbackWithContext, BaseExceptionCallbackImpl):
    def set_context(self, data: dict[str, Any]) -> None:
        self._context = data

    def __call__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: Optional[TracebackType],
    ):
        pass
