import sys
import logging
from app.commands import Command

class ExitCommand(Command):
    def execute(self):
        logging.info("ExitCommand: Exiting application")
        sys.exit("Exiting...")