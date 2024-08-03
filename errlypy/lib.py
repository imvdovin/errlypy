from collections import OrderedDict
from functools import lru_cache, singledispatchmethod
from typing import List, Optional

from errlypy.api import PluginController, Plugin, UninitializedPluginController
from errlypy.internal.event import EventType
from errlypy.internal.event.on_plugin_init import OnPluginInitEvent
from errlypy.internal.event.on_plugin_destroy import OnPluginDestroyEvent


@lru_cache
def get_uninitialized_plugin_controller_singleton() -> "UninitializedPluginController":
    return UninitializedPluginControllerImpl()


@lru_cache
def get_plugin_controller_singleton() -> "PluginController":
    return PluginControllerImpl()


class UninitializedPluginControllerImpl(UninitializedPluginController):
    @staticmethod
    def init(plugins: List[Plugin]) -> PluginController:
        plugin_controller = PluginControllerImpl()
        plugin_controller.register(plugins)

        plugin_init_event = EventType[OnPluginInitEvent]()
        plugin_init_event.notify(OnPluginInitEvent())

        for plugin in plugin_controller.registry.values():
            plugin.setup()

        return plugin_controller


class PluginControllerImpl(PluginController):
    def __init__(self) -> None:
        self._registry = OrderedDict()

    @singledispatchmethod
    def register(self, *args):
        pass

    @register.register
    def _(self, plugin: Plugin) -> None:
        self._set_registry(type(plugin), plugin)

    @register.register
    def _(self, plugins: list) -> None:
        for plugin in plugins:
            self._set_registry(type(plugin), plugin)

    def revert(self) -> UninitializedPluginController:
        plugin_destroy_event = EventType[OnPluginDestroyEvent]()
        plugin_destroy_event.notify(OnPluginDestroyEvent())

        for plugin in self.registry.values():
            plugin.revert()

        return UninitializedPluginControllerImpl()

    def _set_registry(self, key: type, value: Plugin) -> None:
        self._registry.setdefault(key, value)

    @property
    def registry(self):
        return self._registry

    @registry.setter
    def registry(self, _):
        raise Exception("Unable to update registry")


class Errly:
    _plugin_controller: Optional[PluginController] = None

    @classmethod
    def init(
        cls,
        *,
        plugins: List[Plugin],
    ):
        # TODO: Plugins detector
        cls._plugin_controller = UninitializedPluginControllerImpl.init(plugins)
