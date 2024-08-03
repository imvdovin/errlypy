from typing import TypeVar
from errlypy.internal.event import Event, EventType

T = TypeVar("T", bound=EventType)
M = TypeVar("M", bound=Event)


class Observable:
    def notify(self, event_type: T, message: M):
        event_type.notify(message)
