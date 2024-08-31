import aiohttp
from errlypy.django.events import OnDjangoExceptionHasBeenParsedEvent
from errlypy.client.urllib import URLLibClient
from errlypy.internal.config import HTTPErrorConfig


# FIXME: Problem - cannot validate connection (it's valid or not) on init state, not in runtime
class DjangoHTTPCallbackImpl:
    headers = None
    urllib_client = URLLibClient("http://localhost:4000/api")

    @classmethod
    async def send_through_aiohttp(cls, data):
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            session.post(cls.url, json=data)

    @classmethod
    def send_through_urllib(cls, data):
        cls.urllib_client.post(
            HTTPErrorConfig.endpoint,
            {"content": data["error"], "frames": data["frames"]},
        )

    @classmethod
    def notify(cls, event: OnDjangoExceptionHasBeenParsedEvent):
        cls.send_through_urllib(event)
