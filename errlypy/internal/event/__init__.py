import asyncio
import asyncio.coroutines
import inspect
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Dict, Generic, List, Type, TypeVar, Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event:
    event_id: UUID = uuid4()


T = TypeVar("T")
E = TypeVar("E", bound=Event)


class EventType(Generic[T]):
    def __init__(self) -> None:
        self._subscribers: List[
            Union[Callable[[T], None], Callable[[T], Coroutine[Any, Any, None]]]
        ] = []

    def subscribe(
        self,
        callback: Union[Callable[[T], None], Callable[[T], Coroutine[Any, Any, None]]],
    ) -> None:
        self._subscribers.append(callback)

    def unsubscribe(
        self,
        callback: Union[Callable[[T], None], Callable[[T], Coroutine[Any, Any, None]]],
    ) -> None:
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


class EventTypeFactory:
    _instances: Dict[Type, EventType] = {}

    @classmethod
    def get(cls, event_type: Type[E]) -> EventType[E]:
        if event_type not in cls._instances:
            cls._instances[event_type] = EventType[E]()
        return cls._instances[event_type]
