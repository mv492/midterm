"""Tests for the calculator commands (add, sub, mul, div) and the exit command."""

import pytest
import logging
from app.plugins.add import AddCommand
from app.plugins.sub import SubtractCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins.divide import DivideCommand
from app.plugins.exit import ExitCommand


def test_plugin_add_command_valid(capfd, monkeypatch):
    """Test that the AddCommand correctly adds two numbers."""
    inputs = iter(["3", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = AddCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Result: 7.0" in out, "AddCommand output mismatch"

def test_plugin_add_command_invalid(capfd, monkeypatch):
    """Test that the AddCommand handles invalid input gracefully."""
    inputs = iter(["three", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = AddCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Invalid input" in out

def test_plugin_subtract_command_valid(capfd, monkeypatch):
    """Test that the SubtractCommand correctly subtracts two numbers."""
    inputs = iter(["10", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = SubtractCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Result: 6.0" in out, "SubtractCommand output mismatch"

def test_plugin_subtract_command_invalid(capfd, monkeypatch):
    """Test that the SubtractCommand handles invalid input gracefully."""
    inputs = iter(["ten", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = SubtractCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Invalid input" in out

def test_plugin_multiply_command_valid(capfd, monkeypatch):
    """Test that the MultiplyCommand correctly multiplies two numbers."""
    inputs = iter(["3", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = MultiplyCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Result: 15.0" in out, "MultiplyCommand output mismatch"

def test_plugin_multiply_command_invalid(capfd, monkeypatch):
    """Test that the MultiplyCommand handles invalid input gracefully."""
    inputs = iter(["three", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = MultiplyCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Invalid input" in out

def test_plugin_divide_command_valid(capfd, monkeypatch):
    """Test that the DivideCommand correctly divides two numbers."""
    inputs = iter(["20", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = DivideCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Result: 5.0" in out, "DivideCommand output mismatch"

def test_plugin_divide_command_division_by_zero(capfd, monkeypatch):
    """Test that the DivideCommand handles division by zero."""
    inputs = iter(["20", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = DivideCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Division by zero" in out or "not allowed" in out

def test_plugin_divide_command_invalid(capfd, monkeypatch):
    """Test that the DivideCommand handles invalid input gracefully."""
    inputs = iter(["twenty", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    command = DivideCommand()
    command.execute()
    out, _ = capfd.readouterr()
    assert "Invalid input" in out

def test_plugin_exit_command(capfd):
    """Test that the ExitCommand exits the application."""
    command = ExitCommand()
    with pytest.raises(SystemExit) as e:
        command.execute()
    out, _ = capfd.readouterr()
    assert str(e.value) == "Exiting...", "ExitCommand did not exit as expected"
