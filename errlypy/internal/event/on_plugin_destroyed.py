from dataclasses import dataclass

from errlypy.internal.event import Event


@dataclass(frozen=True)
class OnPluginDestroyedEvent(Event):
    pass
