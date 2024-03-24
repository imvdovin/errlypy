from collections import OrderedDict
from functools import lru_cache, singledispatchmethod
from typing import List

from errlypy.api import Integration, IntegrationPlugin


@lru_cache
def get_integration_impl_singleton() -> "IntegrationImpl":
    return IntegrationImpl()


class IntegrationImpl(Integration):
    def __init__(self) -> None:
        self._registry = OrderedDict()
        self._has_setup_been_called = False

    @singledispatchmethod
    def register(self, *args):
        pass

    @register.register
    def _(self, plugin: IntegrationPlugin) -> None:
        self._set_registry(type(plugin), plugin)

    @register.register
    def _(self, plugins: list) -> None:
        for plugin in plugins:
            self._set_registry(type(plugin), plugin)

    def setup(self) -> None:
        if self._has_setup_been_called is True:
            return None

        for plugin in self._registry.values():
            plugin.setup()

        self._has_setup_been_called = True

    def revert(self) -> None:
        if self._has_setup_been_called is False:
            return None

        for plugin in self._registry.values():
            plugin.revert()

        self._has_setup_been_called = False

    def _set_registry(self, key: type, value: IntegrationPlugin) -> None:
        self._registry.setdefault(key, value)


class Errly:
    @classmethod
    def init(
        cls, *, integration=get_integration_impl_singleton(), plugins: List[IntegrationPlugin]
    ):
        integration.register(plugins)
        integration.setup()
