"""Tests for the App functionality."""

import os
import posixpath
import pkgutil
import importlib
import logging
import pytest
from app import App


def test_app_get_environment_variable(monkeypatch):
    """
    Test retrieval of ENVIRONMENT variables. We mock out configure_logging
    so that it doesn't override log settings during the test.
    """
    monkeypatch.setenv('ENVIRONMENT', 'TESTING')
    monkeypatch.setattr("app.App.configure_logging", lambda self: None)

    app = App()
    current_env = app.get_environment_variable('ENVIRONMENT')
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"


def test_app_start_exit_command(capfd, monkeypatch):
    """
    Test that the REPL exits correctly on 'exit' command.
    """
    monkeypatch.setattr("app.App.configure_logging", lambda self: None)
    monkeypatch.setattr('builtins.input', lambda _: 'exit')

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit


def test_app_start_unknown_command(capfd, monkeypatch):
    """
    Test how the REPL handles an unknown command before exiting.
    """
    monkeypatch.setattr("app.App.configure_logging", lambda self: None)

    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit):
        app.start()

    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out


def test_load_plugins_no_directory(monkeypatch, caplog):
    """
    Test that load_plugins() logs a warning when the plugins directory is missing.
    We mock configure_logging so we can capture logs at WARNING or above.
    """
    monkeypatch.setattr("app.App.configure_logging", lambda self: None)

    with caplog.at_level(logging.WARNING, logger="root"):
        app = App()

        orig_exists = os.path.exists
        def fake_exists(path):
            if "app/plugins" in path:
                return False
            return orig_exists(path)

        monkeypatch.setattr(os.path, "exists", fake_exists)

        app.load_plugins()
        # Debug print so you can see what’s in caplog.text if it fails
        print("CAPLOG:", caplog.text)

        assert "Plugins directory 'app/plugins' not found." in caplog.text, (
            "Expected warning about missing plugins directory not logged."
        )


def test_configure_logging_with_conf(monkeypatch, caplog):
    """
    Test configure_logging() branch when a logging.conf file exists.
    Here we allow configure_logging to run so we can test the 'Logging configured' log.
    """
    # We capture INFO logs from the root logger so we can see "Logging configured".
    with caplog.at_level(logging.INFO, logger="root"):
        orig_exists = posixpath.exists

        def fake_exists(path):
            # Return True if checking for 'logging.conf', else use real posixpath.exists
            if path == "logging.conf":
                return True
            return orig_exists(path)

        monkeypatch.setattr(os.path, "exists", fake_exists)
        # We stub out fileConfig so it doesn't try to read a real file
        monkeypatch.setattr(logging.config, "fileConfig", lambda *args, **kwargs: None)

        # Now we DO NOT mock out configure_logging, so it actually runs
        app = App()

        print("CAPLOG:", caplog.text)
        assert "Logging configured" in caplog.text, (
            "Logging configuration message not found in logs."
        )

def test_app_keyboard_interrupt(monkeypatch, caplog):
    """Simulate Ctrl+C and verify that sys.exit(0) is raised and logs are correct."""
    monkeypatch.setattr("app.App.configure_logging", lambda self: None)

    def raise_keyboard_interrupt(_prompt):
        raise KeyboardInterrupt
    monkeypatch.setattr('builtins.input', raise_keyboard_interrupt)

    # Capture at INFO level so we can see logging.info messages
    with caplog.at_level(logging.INFO, logger="root"):
        app = App()
        with pytest.raises(SystemExit) as excinfo:
            app.start()
        assert excinfo.value.code == 0

        # Now check caplog.text instead of stdout
        assert "Application interrupted and exiting gracefully." in caplog.text
        assert "Application shutdown." in caplog.text


def test_load_plugins_import_error(monkeypatch, caplog):
    """
    Test that load_plugins() logs an error when an ImportError occurs.
    We mock out configure_logging so we can capture logs.
    """
    monkeypatch.setattr("app.App.configure_logging", lambda self: None)

    with caplog.at_level(logging.ERROR, logger="root"):
        app = App()

        def mock_import_module(name):
            raise ImportError("Test ImportError")
        monkeypatch.setattr(importlib, "import_module", mock_import_module)

        # Pretend app/plugins exists
        monkeypatch.setattr(os.path, "exists", lambda path: True)
        # Simulate a single plugin named "fake_plugin"
        monkeypatch.setattr(pkgutil, "iter_modules", lambda paths: [(None, "fake_plugin", True)])

        app.load_plugins()
        print("CAPLOG:", caplog.text)

        assert "Error importing plugin fake_plugin: Test ImportError" in caplog.text, (
            "Expected error for plugin import failure not logged."
        )