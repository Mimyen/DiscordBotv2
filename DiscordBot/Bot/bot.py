from __future__ import annotations

import discord
import logging
import requests
import os

from DiscordBot import __version__
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from .Config import config
from .Utils.loghandler import DualHandler
from discord.ext import commands
from dotenv import load_dotenv

# Extensions (Cogs) that are being used
extensions = ['DiscordBot.Bot.Extensions.sync',
              'DiscordBot.Bot.Extensions.pawel',
              'DiscordBot.Bot.Extensions.music',
              'DiscordBot.Bot.Extensions.tictactoe',
              'DiscordBot.Bot.Extensions.tictactoepvp',
              'DiscordBot.Bot.Extensions.stockmarket',
              'DiscordBot.Bot.Extensions.managerapp',
              'DiscordBot.Bot.Extensions.ai',
              'DiscordBot.Bot.Extensions.help',
              'DiscordBot.Bot.Extensions.test',]



class Bot(commands.Bot):
    """
    Class that is the bot itself
    """

    def __init__(self):
        """
        Initializes the bot
        """
        load_dotenv()

        # Setting up schedulers
        scheduler = AsyncIOScheduler()
        scheduler.configure(timezone=utc)

        # Setting up intents
        intents = discord.Intents.all()

        # Initializing the bot
        super().__init__(
            intents=intents,
            command_prefix='?.'
        )



    def run(self):
        """
        Method that is run to start the bot
        """

        token = os.environ.get("DISCORD_TOKEN")

        # Handling the logging
        logger = DualHandler()

        # Running the bot
        super().run(token=token, root_logger=True,
                    reconnect=True, log_handler=logger)



    async def on_ready(self):
        """
        Function is called whever bot is ready
        it's an event function, defaulted by parent
        """

        # Loading each extension
        for extension in extensions:
            try:
                await self.load_extension(extension)
                logging.info(f"Loaded extension {extension}")
            except Exception as e:
                logging.error(f"{e}")

        # Changes bot's status
        activity = discord.Streaming(
            name="Working", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        await super().change_presence(status=discord.Status.idle, activity=activity)

        logging.info(f"Bot is ready!")
