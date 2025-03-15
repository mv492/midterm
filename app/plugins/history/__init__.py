import os
import logging
import pandas as pd

from app.commands import Command

class HistoryCommand(Command):
    """
    A single command handling two sub-commands: 'show' for viewing history,
    and 'clear' for removing all history entries.
    """

    def execute(self):
        """
        Prompt the user for a sub-command ('show' or 'clear') and
        execute the corresponding action.
        """
        sub_command = input("Enter sub-command ('show' or 'clear'): ").strip().lower()

        if sub_command == 'show':
            self.show_history()
        elif sub_command == 'clear':
            self.clear_history()
        else:
            print("Invalid sub-command. Please type 'show' or 'clear'.")

    def show_history(self):
        """
        Display the latest 10 operations from a CSV-based history log.
        """
        history_file = "logs/calculation_history.csv"
        if not os.path.exists(history_file):
            print("No history found.")
            return

        try:
            df = pd.read_csv(history_file)
            if df.empty:
                print("No history found.")
                return

            # Display the last 10 records
            last_10 = df.tail(10)
            print("\n--- Latest 10 Operations ---")
            print(last_10.to_string(index=False))
            print("----------------------------\n")
        except Exception as e:
            logging.error(f"Failed to read history file: {e}")
            print("Error reading history. Please check logs for more details.")

    def clear_history(self):
        """
        Clear the entire calculation history by removing the CSV file.
        """
        history_file = "logs/calculation_history.csv"
        if os.path.exists(history_file):
            try:
                os.remove(history_file)
                logging.info("History cleared.")
                print("History cleared successfully.")
            except Exception as e:
                logging.error(f"Failed to delete history file: {e}")
                print("Error clearing history. Please check logs for more details.")
        else:
            print("No history file found to clear.")
