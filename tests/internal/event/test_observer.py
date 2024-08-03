import pytest
from errlypy.internal.observer import (
    BaseObserverImpl,
    Observer,
    ObserverSubscriberCollectionDto,
)


def test_base_observer_impl_contract_fail():
    with pytest.raises(TypeError) as exc:

        class NotValidObserverClass(BaseObserverImpl):
            pass

    assert exc.type == TypeError


def test_base_observer_impl_contract_success():
    class ValidObserverClass(BaseObserverImpl, Observer):
        @classmethod
        def subscribers(cls) -> ObserverSubscriberCollectionDto:
            return ObserverSubscriberCollectionDto(items=[])

    instance = ValidObserverClass()

    assert isinstance(instance, ValidObserverClass)
