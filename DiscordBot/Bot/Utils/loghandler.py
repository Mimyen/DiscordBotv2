import logging
import discord
import datetime
from ..Config import log


class DualHandler(logging.Handler):
    """
    Class that handles two logging output streams

    file_handler outputs into a newly made file in Temp folder in root of bot

    console_hadler outputs into console, it's colorcoded with discord.py color coding

    all methods are made so everything is setup properly in .run() method in discord.py
    """
    
    def __init__(self, date = True):
        """
        Initializes the class
        """

        super().__init__()

        console_handler = logging.StreamHandler()
        if date: file_handler = logging.FileHandler(filename=f"Temp\\logs\\discord_{datetime.datetime.now().strftime('%d-%m-%Y_%H%M%S')}.log", encoding='utf-8', mode='w')
        else: file_handler = logging.FileHandler(filename=f"Temp\\logs\\discord{log.id()}.log", encoding='utf-8', mode='w')

        self.handlers = [console_handler, file_handler] 



    def emit(self, record):
        """
        Method that edits the messages that will be emitted
        """

        for handler in self.handlers:
            record.msg = self.handler.formatter.format(record)
            handler.emit(record)



    def setFormatter(self, fmt: logging.Formatter | None) -> None:
        """
        Method that sets the formatter for both loggers
        """

        for handler in self.handlers:
            handler.setFormatter(fmt)
        self.handlers[0].setFormatter(discord.utils._ColourFormatter())



    def setLevel(self, level) -> None:
        """
        Method that sets the level of loggers
        """

        for handler in self.handlers:
            handler.setLevel(level)
    
    def addFilter(self, filter) -> None:
        """
        Method that sets filters of loggers
        """

        for handler in self.handlers:
            handler.addFiler(filter)



    def handle(self, record: logging.LogRecord) -> bool:
        """
        Method that handles the record
        """

        for handler in self.handlers:        
            if handler == self.handlers[-1]:
                return handler.handle(record)
            else:
                handler.handle(record)