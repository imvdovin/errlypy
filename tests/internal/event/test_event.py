import asyncio
from uuid import uuid4

import pytest

from errlypy.internal.event import Event
from errlypy.internal.event.type import EventType


@pytest.mark.asyncio
async def test_notify_with_multiple_async_subscribers():
    event_type = EventType[Event]()
    event = Event(event_id=uuid4())

    results = []

    async def async_subscriber_1(event: Event):
        await asyncio.sleep(3)
        results.append(("async_1", asyncio.get_event_loop().time()))

    async def async_subscriber_2(event: Event):
        await asyncio.sleep(2)
        results.append(("async_2", asyncio.get_event_loop().time()))

    async def async_subscriber_3(event: Event):
        await asyncio.sleep(1)
        results.append(("async_3", asyncio.get_event_loop().time()))

    event_type.subscribe(async_subscriber_1)
    event_type.subscribe(async_subscriber_2)
    event_type.subscribe(async_subscriber_3)
    event_type.notify(event)

    await asyncio.sleep(5)

    result_labels = [label for label, _ in results]
    assert result_labels == [
        "async_3",
        "async_2",
        "async_1",
    ], "Async subscribers did not complete in expected order"


@pytest.mark.asyncio
async def test_notify_with_sync_and_multiple_async_subscribers():
    event_type = EventType[Event]()
    event = Event(event_id=uuid4())

    results = []

    def sync_subscriber(event: Event):
        results.append(("sync", asyncio.get_event_loop().time()))

    async def async_subscriber_1(event: Event):
        await asyncio.sleep(3)
        results.append(("async_1", asyncio.get_event_loop().time()))

    async def async_subscriber_2(event: Event):
        await asyncio.sleep(2)
        results.append(("async_2", asyncio.get_event_loop().time()))

    async def async_subscriber_3(event: Event):
        await asyncio.sleep(1)
        results.append(("async_3", asyncio.get_event_loop().time()))

    event_type.subscribe(sync_subscriber)
    event_type.subscribe(async_subscriber_1)
    event_type.subscribe(async_subscriber_2)
    event_type.subscribe(async_subscriber_3)
    event_type.notify(event)

    await asyncio.sleep(5)

    result_labels = [label for label, _ in results]
    assert result_labels[0] == "sync", "Sync subscriber did not complete first"
    assert result_labels[1:] == [
        "async_3",
        "async_2",
        "async_1",
    ], "Async subscribers did not complete in expected order"
