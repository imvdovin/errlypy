from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, List, TypeVar, Union, cast, Type, Generic
from dataclasses import dataclass
from errlypy.internal.event import EventType, EventTypeFactory


T = TypeVar("T", bound=EventType)


@dataclass(frozen=True)
class ObserverSubscriberDto(Generic[T]):
    callback: Union[Callable[[T], None], Callable[[T], Coroutine[Any, Any, None]]]
    event_type: Type[T]


@dataclass(frozen=True)
class ObserverSubscriberCollectionDto:
    items: List[ObserverSubscriberDto]


class Observer(ABC):
    @classmethod
    @abstractmethod
    def subscribers(
        cls,
    ) -> ObserverSubscriberCollectionDto:
        pass


class BaseObserverImpl:
    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)

        if Observer not in cls.__bases__:
            raise TypeError(f"{cls.__name__} should implement {Observer.__name__}")

        BaseObserverImpl._init_subscribers(cast(Observer, cls))

    @staticmethod
    def _init_subscribers(observer: Observer) -> None:
        collection = observer.subscribers()

        if len(collection.items) == 0:
            return None

        for item in collection.items:
            event_type_instance = EventTypeFactory.get(item.event_type)
            event_type_instance.subscribe(item.callback)
