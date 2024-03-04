import discord
import random
import datetime
import logging
from discord.ext import commands
from discord import app_commands
from ..Config.config import *
from discord import Color

# Pawel Extension
class test(commands.Cog):

    # initializing extension
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label="test", style=discord.ButtonStyle.grey)
        async def button_test(self, ctx: discord.Interaction, button: discord.ui.Button):
            await ctx.response.send_message("test", ephemeral=True)

        @discord.ui.button(label="pawelkox", style=discord.ButtonStyle.grey)
        async def button_pawel(self, ctx: discord.Interaction, button: discord.ui.Button):
            await ctx.response.send_message("Pawel jest giga koxem", ephemeral=True)
        

    @app_commands.command(name='test3', description='test3')
    async def command_test3(self, ctx: discord.Interaction) -> None:
        output = discord.Embed()
        output.set_author(name="Tic Tac Toe v1.0", icon_url=ICON_URL)
        output.color = Color.teal()

        await ctx.response.send_message(embed=output, view=self.MyView())

    @app_commands.command(name="getgid", description="Get guild id")
    async def command_getgid(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"{ctx.guild_id}", ephemeral=True)

    @app_commands.command(name="test4", description="asd")
    @app_commands.describe(mention1="Mention an user", mention2="Mention an user")
    async def command_test4(self, ctx: discord.Interaction, mention1: str, mention2: str):
        # await ctx.response.defer(ephemeral=True)
        logging.info(f"test4 {mention1.replace('<','').replace('@','').replace('>','')} {mention2.replace('<','').replace('@','').replace('>','')}")
        await ctx.response.send_message(f"<@{mention1.replace('<','').replace('@','').replace('>','')}> <@{mention2.replace('<','').replace('@','').replace('>','')}>")



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """
    
    await bot.add_cog(test(bot))