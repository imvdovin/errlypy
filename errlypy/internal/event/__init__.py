import asyncio
import asyncio.coroutines
import inspect
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Generic, List, TypeVar, Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event:
    event_id: UUID = uuid4()


T = TypeVar("T")


class EventType(Generic[T]):
    def __init__(self) -> None:
        self._subscribers: List[
            Union[Callable[[T], None], Callable[[T], Coroutine[Any, Any, None]]]
        ] = []

    def subscribe(self, callback: Callable[[T], None]) -> None:
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[T], None]) -> None:
        self._subscribers.remove(callback)

    def notify(self, message: T) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        for subscriber in self._subscribers:
            if inspect.iscoroutinefunction(subscriber):
                if loop:
                    loop.create_task(subscriber(message))
                else:
                    asyncio.run(subscriber(message))
            else:
                subscriber(message)
