import discord
import random
import datetime
import logging
from discord.ext import commands
from discord import app_commands
from ..Config.config import *
from discord import Color



class slashHelp(commands.Cog):
    """
    Extension that adds /help command to the bot
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes the extension
        """

        self.bot = bot

    @app_commands.command(name=COMMAND_HELP_NAME, description=COMMAND_HELP_DESCRIPTION)
    async def command_help(self, ctx: discord.Interaction) -> None:
        """
        Method that is run after using /help

        Outputs all commands and their descriptions
        except ones included in COMMAND_HELP_IGNORED_COMMANDS
        (this list is editable in config)
        """
        commands = await self.bot.tree.sync()

        ignore = COMMAND_HELP_IGNORED_COMMANDS

        index = 1
        output = discord.Embed()
        output.description = ""

        for command in commands:

            if command.name not in ignore:
                output.description += f"{index}. **{command.name}** - {command.description}\n"
                index += 1

        output.color = Color.green()
        output.set_author(name="Help", icon_url=ICON_URL)

        await ctx.response.send_message(ephemeral=True, embed=output)



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """

    await bot.add_cog(slashHelp(bot))
