from collections import OrderedDict
from functools import lru_cache, singledispatchmethod
from typing import List, Optional
from uuid import uuid4

from errlypy.api import Plugin, PluginController, UninitializedPluginController
from errlypy.internal.event.type import EventType
from errlypy.internal.event.on_plugin_destroyed import OnPluginDestroyedEvent
from errlypy.internal.event.on_plugin_initialized import OnPluginInitializedEvent


@lru_cache
def get_uninitialized_plugin_controller_singleton() -> "UninitializedPluginController":
    return UninitializedPluginControllerImpl()


@lru_cache
def get_plugin_controller_singleton() -> "PluginController":
    return PluginControllerImpl()


class UninitializedPluginControllerImpl(
    UninitializedPluginController,
):
    @staticmethod
    def init(plugins: List[Plugin]) -> PluginController:
        plugin_controller = PluginControllerImpl()
        plugin_controller.register(plugins)

        on_initialized_event_instance = EventType[OnPluginInitializedEvent]()

        for plugin in plugin_controller.registry.values():
            plugin.setup()
            on_initialized_event_instance.notify(
                OnPluginInitializedEvent(event_id=uuid4()),
            )

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
        on_destroyed_event_instance = EventType[OnPluginDestroyedEvent]()

        for plugin in self.registry.values():
            plugin.revert()
            on_destroyed_event_instance.notify(
                OnPluginDestroyedEvent(event_id=uuid4()),
            )

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
