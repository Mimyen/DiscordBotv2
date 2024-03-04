import os

from DiscordBot import __version__
from DiscordBot.Bot.bot import Bot

# It think it's for unix systems don't ask
if os.name != "nt":
    import uvloop
    uvloop.install()

# Initializing and running the bot
if __name__ == "__main__":
    bot = Bot()
    bot.run()
