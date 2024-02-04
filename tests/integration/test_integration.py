from unittest.mock import patch
from errlypy.integrations.api import IntegrationPlugin
from errlypy.integrations.integration import (
    IntegrationImpl,
    get_integration_impl_singleton,
)


class TestIntegrationPluginImpl(IntegrationPlugin):
    def setup(self) -> None:
        pass

    def revert(self) -> None:
        pass

    def __call__(self, *args, **kwargs):
        pass


class AnotherTestIntegrationPluginImpl(IntegrationPlugin):
    def setup(self) -> None:
        pass

    def revert(self) -> None:
        pass

    def __call__(self, *args, **kwargs):
        pass


def test_integration_singleton_function():
    first_integration = get_integration_impl_singleton()
    second_integration = get_integration_impl_singleton()

    assert first_integration is second_integration


def test_integration_register_plugin():
    plugin = TestIntegrationPluginImpl()
    integration = IntegrationImpl()

    integration.register(plugin)

    assert integration._registry[type(plugin)] is plugin


def test_integration_register_plugins():
    plugins = [
        TestIntegrationPluginImpl(),
        AnotherTestIntegrationPluginImpl(),
    ]
    integration = IntegrationImpl()

    integration.register(plugins)

    assert integration._registry[type(plugins[0])] is plugins[0]
    assert integration._registry[type(plugins[1])] is plugins[1]


def test_integration_setup_plugin():
    plugin = TestIntegrationPluginImpl()
    integration = IntegrationImpl()

    with patch.object(plugin, "setup", wraps=plugin.setup) as wrapped_setup:
        integration.register(plugin)
        integration.setup()

        assert wrapped_setup.call_count == 1


def test_integration_setup_plugins():
    plugins = [
        TestIntegrationPluginImpl(),
        AnotherTestIntegrationPluginImpl(),
    ]
    integration = IntegrationImpl()

    with patch.object(
        plugins[0], "setup", wraps=plugins[0].setup
    ) as wrapped_setup_first, patch.object(
        plugins[1], "setup", wraps=plugins[1].setup
    ) as wrapped_setup_second:
        integration.register(plugins)
        integration.setup()

        assert wrapped_setup_first.call_count == 1
        assert wrapped_setup_second.call_count == 1


def test_integration_revert_plugin():
    plugin = TestIntegrationPluginImpl()
    integration = IntegrationImpl()

    with patch.object(plugin, "revert", wraps=plugin.revert) as wrapped_revert:
        integration.register(plugin)
        integration.setup()
        integration.revert()

        assert wrapped_revert.call_count == 1


def test_integration_revert_plugins():
    plugins = [
        TestIntegrationPluginImpl(),
        AnotherTestIntegrationPluginImpl(),
    ]
    integration = IntegrationImpl()

    with patch.object(
        plugins[0], "revert", wraps=plugins[0].revert
    ) as wrapped_revert_first, patch.object(
        plugins[1], "revert", wraps=plugins[1].revert
    ) as wrapped_revert_second:
        integration.register(plugins)
        integration.setup()
        integration.revert()

        assert wrapped_revert_first.call_count == 1
        assert wrapped_revert_second.call_count == 1


def test_integration_setup_plugin_twice():
    plugin = TestIntegrationPluginImpl()
    integration = IntegrationImpl()

    with patch.object(plugin, "setup", wraps=plugin.setup) as wrapped_setup:
        integration.register(plugin)

        for _ in range(2):
            integration.setup()

        assert wrapped_setup.call_count == 1


def test_integration_setup_plugins_twice():
    plugins = [
        TestIntegrationPluginImpl(),
        AnotherTestIntegrationPluginImpl(),
    ]
    integration = IntegrationImpl()

    with patch.object(
        plugins[0], "setup", wraps=plugins[0].setup
    ) as wrapped_revert_first, patch.object(
        plugins[1], "setup", wraps=plugins[1].setup
    ) as wrapped_revert_second:
        integration.register(plugins)

        for _ in range(2):
            integration.setup()

        assert wrapped_revert_first.call_count == 1
        assert wrapped_revert_second.call_count == 1


def test_integration_revert_plugin_twice():
    plugin = TestIntegrationPluginImpl()
    integration = IntegrationImpl()

    with patch.object(plugin, "revert", wraps=plugin.revert) as wrapped_revert:
        integration.register(plugin)
        integration.setup()

        for _ in range(2):
            integration.revert()

        assert wrapped_revert.call_count == 1


def test_integration_revert_plugins_twice():
    plugins = [
        TestIntegrationPluginImpl(),
        AnotherTestIntegrationPluginImpl(),
    ]
    integration = IntegrationImpl()

    with patch.object(
        plugins[0], "revert", wraps=plugins[0].revert
    ) as wrapped_revert_first, patch.object(
        plugins[1], "revert", wraps=plugins[1].revert
    ) as wrapped_revert_second:
        integration.register(plugins)
        integration.setup()

        for _ in range(2):
            integration.revert()

        assert wrapped_revert_first.call_count == 1
        assert wrapped_revert_second.call_count == 1
