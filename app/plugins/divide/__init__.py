import os
import logging
import pandas as pd
from datetime import datetime

from app.commands import Command

class DivideCommand(Command):
    def execute(self):
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            # Handle divide-by-zero
            if b == 0:
                logging.error("DivideCommand: Attempt to divide by zero.")
                print("Error: Cannot divide by zero.")
                return

            result = a / b
            logging.info("DivideCommand: %s / %s = %s", a, b, result)
            print(f"Result: {result}")

            self.save_to_history("divide", a, b, result)
        except ValueError:
            logging.error("DivideCommand: Invalid input encountered")
            print("Invalid input. Please enter numeric values.")

    def save_to_history(self, operation, a, b, result):
        history_file = "logs/calculation_history.csv"

        if os.path.exists(history_file):
            df = pd.read_csv(history_file)
        else:
            df = pd.DataFrame(columns=["timestamp", "operation", "operands", "result"])

        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "operands": f"{a}, {b}",
            "result": result
        }

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(history_file, index=False)
