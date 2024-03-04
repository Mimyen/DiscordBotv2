import discord
import random
import datetime
import logging
from discord.ext import commands
from discord import app_commands
from ..Config.config import *


# Pawel Extension
class Pawel(commands.Cog):

    # initializing extension
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "pawel kox" in message.content.lower():
            await message.reply("rel")
        # elif "pawel" in message.content.lower() and message.guild.id == 1050720582267838494:
        #     emoji = discord.utils.get(self.bot.emojis, name="rare_happy_pawel")
        #     await message.add_reaction("🇵")
        #     await message.add_reaction("🇦")
        #     await message.add_reaction("🇼")
        #     await message.add_reaction("🇪")
        #     await message.add_reaction("🇱")
        #     await message.add_reaction("🇰")
        #     await message.add_reaction("🇴")
        #     await message.add_reaction("🇽")
        #     await message.add_reaction(emoji)

    # definition of /ile command that responds with random int from <0,300> range

    @app_commands.command(name=COMMAND_ILE_NAME, description=COMMAND_ILE_DESCRIPTION)
    async def command_ile(self, ctx: discord.interactions.Interaction):
        await ctx.response.send_message(COMMAND_ILE_P1 + str(random.randint(0, 300)) + COMMAND_ILE_P2)

    # command that finds out if two people love each other
    @app_commands.command(name=COMMAND_MILOSC_NAME, description=COMMAND_MILOSC_DESCRIPTION)
    @app_commands.describe(imie1=COMMAND_MILOSC_IMIE1, imie2=COMMAND_MILOSC_IMIE2)
    async def command_milosc(self, ctx: discord.interactions.Interaction, imie1: str, imie2: str) -> None:
        if ((imie1 in ["pawel", "Pawel", "paweł", "Paweł"] and imie2 in ["Ola", "ola"]) or (imie2 in ["pawel", "Pawel", "paweł", "Paweł"] and imie1 in ["Ola", "ola"])
            or (imie2 in ["lukasz", "Lukasz", "Łukasz", "łukasz"] and imie1 in ["Wiktoria", "wiktoria", "Viktoriia", "viktoriia", "viktoria", "Viktoria"])
                or (imie1 in ["lukasz", "Lukasz", "Łukasz", "łukasz"] and imie2 in ["Wiktoria", "wiktoria", "Viktoriia", "viktoriia", "viktoria", "Viktoria"])):
            await ctx.response.send_message(imie1 + " i " + imie2 + " " + COMMAND_MILOSC_ODPOWIEDZI[2])
        else:
            await ctx.response.send_message(imie1 + " i " + imie2 + " " + COMMAND_MILOSC_ODPOWIEDZI[random.randint(0, 1)])

    # command that outputs what pawel we have today
    @app_commands.command(name=COMMAND_PAWELNADZIS_NAME, description=COMMAND_PAWELNADZIS_DESCRIPTION)
    async def command_pawel_na_dzis(self, ctx: discord.interactions.Interaction) -> None:
        await ctx.response.send_message(COMMAND_PAWELNADZIS_TEKST + COMMAND_PAWELNADZIS_PAWLY[datetime.datetime.now().day % len(COMMAND_PAWELNADZIS_PAWLY)])

# Adding exntension to the bot
async def setup(bot):
    await bot.add_cog(Pawel(bot))
