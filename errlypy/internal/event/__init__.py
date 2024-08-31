from dataclasses import dataclass
from uuid import UUID


# Since 3.10 we can use kw_only feature
@dataclass(frozen=True)
class Event:
    event_id: UUID
