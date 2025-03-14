import sys
import logging
from app.commands import Command


class MultiplyCommand(Command):
    def execute(self):
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            result=a*b
            logging.info("MultiplyCommand: %s * %s = %s", a, b, result)
            print(f"Result: {result}")
        except ValueError:
            logging.error("MultiplyCommand: Invalid input encountered")
            print("Invalid input. Please enter numeric values.")