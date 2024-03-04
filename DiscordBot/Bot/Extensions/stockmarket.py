import discord
import random
import datetime
import os
import logging
import requests
import numpy as np
import matplotlib.pyplot as plt

from discord.ext import commands
from discord import app_commands
from ..Config.config import *
from discord import Color
from dotenv import load_dotenv


class stockMarket(commands.Cog):
    """
    stockMarket extension lets user draw a graph that shows value of cryptocurrency in real currency in time
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializing the extension
        """

        self.bot = bot



    @app_commands.command(name="crypto", description="Get graph of certain cryptocurrency")
    @app_commands.describe(symbol="Symbol of cryptocurrency", exchange="Real currency that cryptocurrency will be compared to", start_date="Date since which the graph will be displaying data")
    async def command_crypto(self, ctx: discord.Interaction, symbol: str, exchange: str, start_date: str) -> None:
        """
        Command that draws graph that represents price of `symbol` in `exchange` since `start_date`

        `symbol` is str ('BTC')

        `exchange` is str ('USD')

        `start_date` is str represeting date in format 'RRRR-MM-DD' ('2022-01-01')
        """

        await ctx.response.defer()

        api_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={exchange}&apikey={os.environ.get("SM_API_KEY")}'
        raw_df = requests.get(api_url).json()

        x = []
        y = []

        for key in raw_df['Time Series (Digital Currency Daily)']:
            if key >= start_date:
                x.append(key)
                y.append(float(raw_df['Time Series (Digital Currency Daily)'][key][f'1a. open ({exchange})']))
        

        x1 = [datetime.datetime.strptime(date_str, '%Y-%m-%d') for date_str in x]
        
        # Set custom RGB colors for plot elements
        line_color = (0.1019607843, 188/255, 156/255)  
        background_color = (0.168627451, 0.1764705882, 0.1921568627) 
        label_color = (0.8156862745, 0.8705882353, 0.8823529412)
        grid_color = (0.5, 0.5, 0.5)

        fig, ax = plt.subplots()
        ax.plot(x1[::-1], y[::-1], color=line_color, linewidth=3)
        ax.fill_between(x1[::-1], y[::-1], color=line_color, alpha=0.2)
        ax.set(xlabel='', ylabel='', title=f'')

        
        # Customize other elements
        ax.set_facecolor(background_color)
        ax.xaxis.label.set_color(label_color)
        ax.yaxis.label.set_color(label_color)
        ax.title.set_color(label_color)
        ax.tick_params(axis='x', colors=label_color, rotation=45) 
        ax.tick_params(axis='y', colors=label_color)
        ax.spines['bottom'].set_color(label_color)
        ax.spines['top'].set_color(label_color)
        ax.spines['right'].set_color(label_color)
        ax.spines['left'].set_color(label_color)
        ax.grid(color=grid_color)
        ax.margins(x=0)

        min_y = min(y)
        max_y = max(y)

        # Set y-axis limits to display relevant part of the graph
        ax.set_ylim(min_y - (max_y - min_y) * 0.1, max_y + (max_y - min_y) * 0.1)

        fig.tight_layout(pad=0, h_pad=0, w_pad=0) 

        fig.savefig(f"{CRYPTO_PATH}{symbol}{exchange}.png", facecolor=background_color)

        file = discord.File(f"{CRYPTO_PATH}{symbol}{exchange}.png", "graph.png")

        output = discord.Embed()
        output.set_author(name=f"Price of {symbol} in {exchange} since {start_date}", icon_url=ICON_URL)
        output.set_image(url=f"attachment://{file.filename}")
        output.set_footer(text="Dates are in format YYYY-MM-DD")
        output.color = Color.teal()

        await ctx.edit_original_response(embed=output, attachments=[file])



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """
    
    await bot.add_cog(stockMarket(bot))
