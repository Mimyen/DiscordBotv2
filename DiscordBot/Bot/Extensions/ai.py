import discord
import random
import datetime
import logging
import os
from discord.ext import commands
from discord import app_commands
from ..Config.config import *
from discord import Color
from openai import OpenAI
from dotenv import load_dotenv


class ai(commands.Cog):
    """
    AI extension let's the bot user ask open-ai anything they want to know about
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializing AI extension
        """
        load_dotenv()

        self.bot = bot
        self.client = OpenAI(api_key=os.environ.get("AI_API_KEY"))



    @app_commands.command(name=COMMAND_GPTASK_NAME, description=COMMAND_GPTASK_DESCRIPTION)
    @app_commands.describe(query=COMMAND_GPTASK_QUERY)
    async def command_gptask(self, ctx: discord.Interaction, query: str) -> None:
        """
        Command that let's you ask openai anything you want
        """
        await ctx.response.defer()

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": GPT_DEFAULT_SETTINGS},
                {"role": "user", "content": query}
            ]
        )

        output = discord.Embed()
        output.set_author(name=f"Question: {query}", icon_url=ICON_URL)
        output.description = completion.choices[0].message.content
        output.color = Color.teal()
        output.set_footer(text=f"Question asked by {ctx.user.nick}")

        await ctx.edit_original_response(embed=output)



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """
    
    await bot.add_cog(ai(bot))
