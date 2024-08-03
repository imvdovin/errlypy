from types import TracebackType
from typing import Optional, Type
import pytest
from unittest import mock
from django.urls import reverse
from werkzeug.test import Client
from errlypy.api import ExceptionCallback
from errlypy.lib import Errly
from errlypy.django.plugin import DjangoExceptionPlugin
from errlypy.django.events import OnDjangoExceptionHasBeenParsedEvent
from errlypy.internal.observer import (
    BaseObserverImpl,
    Observer,
    ObserverSubscriberDto,
    ObserverSubscriberCollectionDto,
)
from tests.django.mysite.wsgi import application


@pytest.fixture
def client():
    return Client(application)


class TestExceptionCallback(ExceptionCallback):
    def set_next(self, callback: ExceptionCallback) -> ExceptionCallback:
        return callback

    def __call__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: Optional[TracebackType],
    ):
        return exc_type, exc_value, exc_traceback


def test_view_zero_division(client):
    django_plugin = DjangoExceptionPlugin()
    Errly.init(plugins=[django_plugin])
    mock_callback = mock.MagicMock()

    class TestObserver(BaseObserverImpl, Observer):
        @classmethod
        def subscribers(cls) -> ObserverSubscriberCollectionDto:
            return ObserverSubscriberCollectionDto(
                items=[
                    ObserverSubscriberDto(
                        callback=mock_callback,
                        event_type=OnDjangoExceptionHasBeenParsedEvent,
                    )
                ]
            )

    result = client.get(reverse("view_zero_division"))

    assert result.status_code == 500
    # assert mock_callback.call_count == 1
    result = mock_callback.call_args[0][0]
    assert result["data"][0].function == "view_zero_division"
    assert result["data"][0].line == "1 / 0"
