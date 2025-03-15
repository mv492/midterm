"""Tests for the calculator commands (add, sub, mul, div) and the exit command."""

import pytest
import logging
import os
import pytest
import pandas as pd
from app.plugins.history import HistoryCommand
from app.plugins.add import AddCommand
from app.plugins.sub import SubtractCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins.divide import DivideCommand
from app.plugins.exit import ExitCommand

HISTORY_FILE = "logs/calculation_history.csv"


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
    assert "Error: Cannot divide by zero." in out

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

@pytest.fixture
def cleanup_history_file():
    """
    This fixture removes the history file before and after each test,
    ensuring a clean test environment.
    """
    # Remove if it exists before the test
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

    yield

    # Remove if it exists after the test
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


def test_plugin_history_command_show_no_file(capfd, monkeypatch, cleanup_history_file):
    """Test that the HistoryCommand sub-command 'show' indicates no history if the file doesn't exist."""
    # When prompted for a sub-command, input 'show'
    user_inputs = iter(["show"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    command = HistoryCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert "No history found" in out, "Expected a 'No history found.' message when file is missing."


def test_plugin_history_command_show_with_data(capfd, monkeypatch, cleanup_history_file):
    """Test that 'show' displays the last 10 operations if the CSV file exists and has data."""
    # Create a fake CSV file with 3 sample records
    data = {
        "timestamp": ["2025-03-15 10:00:00", "2025-03-15 10:01:00", "2025-03-15 10:02:00"],
        "operation": ["add", "subtract", "multiply"],
        "operands": ["3, 4", "10, 4", "2, 8"],
        "result": [7, 6, 16]
    }
    df = pd.DataFrame(data)
    os.makedirs("logs", exist_ok=True)
    df.to_csv(HISTORY_FILE, index=False)

    # Input 'show'
    user_inputs = iter(["show"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    command = HistoryCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert "2025-03-15 10:00:00" in out, "Expected the first record to appear in output."
    assert "multiply" in out, "Expected 'multiply' operation to appear in output."


def test_plugin_history_command_clear_no_file(capfd, monkeypatch, cleanup_history_file):
    """Test that the HistoryCommand sub-command 'clear' indicates no file to clear if missing."""
    # Input 'clear'
    user_inputs = iter(["clear"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    command = HistoryCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert "No history file found" in out, "Expected a message indicating there's no file to clear."


def test_plugin_history_command_clear_with_file(capfd, monkeypatch, cleanup_history_file):
    """Test that 'clear' removes the CSV file if it exists."""
    # Create an empty CSV file to simulate existing history
    os.makedirs("logs", exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("timestamp,operation,operands,result\n")

    # Input 'clear'
    user_inputs = iter(["clear"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    command = HistoryCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert "History cleared successfully" in out, "Expected success message after clearing."
    assert not os.path.exists(HISTORY_FILE), "CSV file should be removed upon clearing."
