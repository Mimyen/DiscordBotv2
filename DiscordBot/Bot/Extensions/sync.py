import logging
import os

from discord.ext import commands
from ..Config.config import *
from dotenv import load_dotenv


class Sync(commands.Cog):
    """
    Sync extension is used for syncronizing commands with discord
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes the extension
        """
        load_dotenv()

        self.bot = bot

    @commands.command()
    async def sync(self, ctx: commands.Context) -> None:
        """
        Method that syncronizes bot commands with discord
        """

        fmt = await ctx.bot.tree.sync()
        if ctx.author.id == int(os.environ.get("OWNER_ID")):
            await ctx.send(f"Synced {len(fmt)} commands", delete_after=3.0)
            await ctx.message.delete()
            logging.info(COMMAND_SYNC_SYNCHRONIZING)
        return



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """
    
    await bot.add_cog(Sync(bot))