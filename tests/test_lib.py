from unittest.mock import patch

import pytest

from errlypy.api import Plugin
from errlypy.lib import (
    PluginControllerImpl,
    UninitializedPluginControllerImpl,
    get_plugin_controller_singleton,
)


class TestPluginImpl(Plugin):
    def setup(self) -> None:
        pass

    def revert(self) -> None:
        pass

    def __call__(self, *args, **kwargs):
        pass


class AnotherTestPluginImpl(Plugin):
    def setup(self) -> None:
        pass

    def revert(self) -> None:
        pass

    def __call__(self, *args, **kwargs):
        pass


@pytest.fixture(scope="function")
def plugins():
    return [
        TestPluginImpl(),
        AnotherTestPluginImpl(),
    ]


@pytest.fixture(scope="function")
def plugin():
    return TestPluginImpl()


def test_plugin_controller_singleton_function():
    first_plugin_controller = get_plugin_controller_singleton()
    second_plugin_controller = get_plugin_controller_singleton()

    assert first_plugin_controller is second_plugin_controller


def test_plugin_controller_register_plugin():
    plugin = TestPluginImpl()
    plugin_controller = PluginControllerImpl()

    plugin_controller.register(plugin)

    assert plugin_controller._registry[type(plugin)] is plugin


def test_plugin_controller_register_plugins():
    plugins = [
        TestPluginImpl(),
        AnotherTestPluginImpl(),
    ]
    plugin_controller = PluginControllerImpl()

    plugin_controller.register(plugins)

    assert plugin_controller._registry[type(plugins[0])] is plugins[0]
    assert plugin_controller._registry[type(plugins[1])] is plugins[1]


def test_plugin_controller_setup_plugin():
    plugin = TestPluginImpl()

    with patch.object(plugin, "setup", wraps=plugin.setup) as wrapped_setup:
        UninitializedPluginControllerImpl.init([plugin])

        assert wrapped_setup.call_count == 1


def test_plugin_controller_setup_plugins(plugins):
    with patch.object(
        plugins[0], "setup", wraps=plugins[0].setup
    ) as wrapped_setup_first, patch.object(
        plugins[1], "setup", wraps=plugins[1].setup
    ) as wrapped_setup_second:
        UninitializedPluginControllerImpl.init(plugins)

        assert wrapped_setup_first.call_count == 1
        assert wrapped_setup_second.call_count == 1


def test_plugin_controller_revert_plugin(plugin):
    with patch.object(plugin, "revert", wraps=plugin.revert) as wrapped_revert:
        plugin_controller = UninitializedPluginControllerImpl.init([plugin])
        plugin_controller.revert()

        assert wrapped_revert.call_count == 1


def test_plugin_controller_revert_plugins(plugins):
    with patch.object(
        plugins[0], "revert", wraps=plugins[0].revert
    ) as wrapped_revert_first, patch.object(
        plugins[1], "revert", wraps=plugins[1].revert
    ) as wrapped_revert_second:
        plugin_controller = UninitializedPluginControllerImpl.init(plugins)
        plugin_controller.revert()

        assert wrapped_revert_first.call_count == 1
        assert wrapped_revert_second.call_count == 1
