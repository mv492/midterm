import sys
import logging
from app.commands import Command

class AddCommand(Command):
    def execute(self):
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            result=a+b
            logging.info("AddCommand: %s + %s = %s", a, b, result)
            print(f"Result: {result}")
        except ValueError:
            logging.error("AddCommand: Invalid input encountered")
            print("Invalid input. Please enter numeric values.")