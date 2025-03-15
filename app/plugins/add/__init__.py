import os
import logging
import pandas as pd
from datetime import datetime

from app.commands import Command

class AddCommand(Command):
    def execute(self):
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            result = a + b
            logging.info("AddCommand: %s + %s = %s", a, b, result)
            print(f"Result: {result}")

            # Write the operation to the CSV history
            self.save_to_history("add", a, b, result)
        except ValueError:
            logging.error("AddCommand: Invalid input encountered")
            print("Invalid input. Please enter numeric values.")

    def save_to_history(self, operation, a, b, result):
        """
        Appends a new record to logs/calculation_history.csv.
        Columns: timestamp, operation, operands, result
        """
        history_file = "logs/calculation_history.csv"

        # Load existing data if it exists, otherwise create a new DataFrame
        if os.path.exists(history_file):
            df = pd.read_csv(history_file)
        else:
            df = pd.DataFrame(columns=["timestamp", "operation", "operands", "result"])

        # Create a new entry
        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "operands": f"{a}, {b}",
            "result": result
        }

        # Append the new row and save
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(history_file, index=False)
