from dataclasses import dataclass

from errlypy.internal.event import Event
from errlypy.exception import ParsedExceptionDto


@dataclass(frozen=True)
class OnDjangoExceptionHasBeenParsedEvent(Event):
    data: ParsedExceptionDto
