from types import TracebackType
from typing import Optional, Type

import pytest
from django.urls import reverse
from werkzeug.test import Client

from errlypy.api import ExceptionCallback
from errlypy.django import DjangoExceptionPlugin
from errlypy.django.events import OnDjangoExceptionHasBeenParsedEvent
from errlypy.internal.event.type import EventType
from errlypy.lib import Errly
from tests.django.mysite.wsgi import application


@pytest.fixture
def client():
    return Client(application)


@pytest.fixture
def on_exc_parsed_fixture():
    return EventType[OnDjangoExceptionHasBeenParsedEvent]()


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


def test_view_zero_division(client, on_exc_parsed_fixture):
    django_plugin = DjangoExceptionPlugin(on_exc_parsed_fixture)
    Errly.init(plugins=[django_plugin])

    result = client.get(reverse("view_zero_division"))

    assert result.status_code == 500
