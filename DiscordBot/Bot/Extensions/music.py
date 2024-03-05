from ast import alias
import discord
import datetime
import logging
import asyncio
import os
from youtubesearchpython import VideosSearch
from discord.ext import commands
from discord import app_commands
from ..Config.config import *
from yt_dlp import YoutubeDL
from discord import Color
from dotenv import load_dotenv



class Music(commands.Cog):
    """
    Music extension lets users play music on discord server
    """
  
    def __init__(self, bot: commands.Bot):
        """
        Initializing Music Extension
        """

        load_dotenv()

        self.OWNER_ID = os.environ.get("OWNER_ID")

        self.bot = bot

        # { guild_id : [ voicechannel_id, channel_id , playlist=[], isPlaying, Timer, CurrentSong ] }
        self.guildInfo = {}

        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)



    class LinkException(Exception):
        """
        Class responsible for making exception thrown whenever incorrect link is supplied
        """

        def __init__(self, message: str =LINKEXCEPTION):
            """
            Initializing link exception
            """

            self.message = message
            super().__init__(self.message)



    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        """
        Supposed to be enabling only owner to be able to use connect and disconnect commands

        Sadly doesn't work
        """

        if msg["t"] == "INTERACTION_CREATE":
            data = msg["d"]
            command_name = data["data"]["name"]
            if command_name == "disconnect" and data["member"]["user"]["id"] == self.OWNER_ID:
                command_id = data["id"]
                await self.bot.http.edit_application_command_permissions(self.bot.user.id, self.bot.application_id, command_id, [
                    {
                        "id": self.OWNER_ID,
                        "type": 1,
                        "permission": True
                    }
                ])
            elif command_name == "connect" and data["member"]["user"]["id"] == self.OWNER_ID:
                command_id = data["id"]
                await self.bot.http.edit_application_command_permissions(self.bot.user.id, self.bot.application_id, command_id, [
                    {
                        "id": self.OWNER_ID,
                        "type": 1,
                        "permission": True
                    }
                ])



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        Method that updates voice channel that bot is currently in
        """
        
        if member == self.bot.user:
            if before.channel != after.channel:
                if after.channel is not None:
                    self.guildInfo[after.channel.guild.id][0] = after.channel
                else:
                    logging.info(LISTENER_ONMOVE_DISCONNECT)



    def search_yt(self, item):
        """
        Method that searches youtube for correct video according to description in supplied query
        """
        
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return {'source': item, 'title': title}

        search = VideosSearch(item, limit=1)

        return {'source': search.result()["result"][0]["link"], 'title': search.result()["result"][0]["title"]}
    


    async def play_next(self, ctx: discord.Interaction):
        """
        Method that plays next song in queue
        """

        if len(self.guildInfo[ctx.guild_id][2]) > 0:

            self.guildInfo[ctx.guild_id][3] = True

            m_url = self.guildInfo[ctx.guild_id][2][0]['source']

            self.guildInfo[ctx.guild_id][5] = self.guildInfo[ctx.guild_id][2][0]
            self.guildInfo[ctx.guild_id][2].pop(0)

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))

            song = data['url']
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(song, executable="Bin\\ffmpeg.exe", **self.FFMPEG_OPTIONS),
                                        after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

        else:
            self.guildInfo[ctx.guild_id][3] = False



    async def play_music(self, ctx: discord.Interaction):
        """
        Method that starts playing songs
        """

        if len(self.guildInfo[ctx.guild_id][2]) > 0:

            self.guildInfo[ctx.guild_id][3] = True

            m_url = self.guildInfo[ctx.guild_id][2][0]['source']

            self.guildInfo[ctx.guild_id][5] = self.guildInfo[ctx.guild_id][2][0]
            self.guildInfo[ctx.guild_id][2].pop(0)

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))

            song = data['url']
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(song, executable="Bin\\ffmpeg.exe", **self.FFMPEG_OPTIONS),
                                        after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

        else:

            self.guildInfo[ctx.guild_id][3] = False



    async def connect(self, ctx: discord.interactions.Interaction) -> bool:
        """
        Method that connects bot to voice channel

        In addition it sets up necessary variables 
        """

        try:
            if self.guildInfo[ctx.guild_id] or ctx.user.voice.channel == None:
                if ctx.guild.voice_client is not None and ctx.user.voice.channel != self.guildInfo[ctx.guild_id][0]:
                    await ctx.guild.voice_client.move_to(ctx.user.voice.channel)
                return True

        except Exception as e:
            try:

                self.guildInfo[ctx.guild_id] = [
                    ctx.user.voice.channel,
                    ctx.channel_id,
                    [],
                    False,
                    datetime.datetime.now(),
                    {'title': "", 'source': ""}
                ]

                await self.guildInfo[ctx.guild_id][0].connect()

                return True

            except Exception as ee:

                return False



    async def disconnect(self, ctx: discord.interactions.Interaction) -> bool:
        """
        Method that disconnects bot from voice channel

        In addition it deletes unnecessary stored data
        """
        
        try:
            if self.guildInfo[ctx.guild_id]:
                self.guildInfo.pop(ctx.guild_id)
                await ctx.guild.voice_client.disconnect()
                return True
        except Exception as e:
            logging.error(f"{e}")
            return False



    @app_commands.command(name=COMMAND_CONNECT_NAME, description=COMMAND_CONNECT_DESCRIPTION)
    async def command_connect(self, ctx: discord.Interaction) -> None:
        """
        Command that connects bot to the voice channel
        """
        
        if await self.connect(ctx):
            await ctx.response.send_message(COMMAND_CONNECT_CONNECTED)
        else:
            await ctx.response.send_message(COMMAND_CONNECT_ERROR)

 
    @app_commands.command(name=COMMAND_DISCONNECT_NAME, description=COMMAND_DISCONNECT_DESCRIPTION)
    async def command_disconnect(self, ctx: discord.Interaction) -> None:
        """
        Command that disconnects the bot from a voice channel
        """
        
        if await self.disconnect(ctx):
            await ctx.response.send_message(COMMAND_DISCONNECT_DISCONNECTED)
        else:
            await ctx.response.send_message(COMMAND_DISCONNECT_NO_VC)



    @app_commands.command(name=COMMAND_PLAY_NAME, description=COMMAND_PLAY_DESCRIPTION)
    @app_commands.describe(query=COMMAND_PLAY_QUERY)
    async def command_play(self, ctx: discord.Interaction, query: str) -> None:
        """
        Command that makes the bot begin playing in a voiche channel
        or adds next song to the queue
        """

        output = discord.Embed()
        try:
            if await self.connect(ctx):
                try:
                    song = self.search_yt(query)
                    if type(song) == type(True):
                        output.color = Color.red()
                        output.description = LINKEXCEPTION
                        await ctx.response.send_message(embed=output, ephemeral=True)
                        return
                    output.color = Color.green()
                    if self.guildInfo[ctx.guild_id][3] == False:
                        self.guildInfo[ctx.guild_id][2].append(song)
                        output.set_author(
                            name=COMMAND_PLAY_PLAYING, icon_url=ICON_URL)
                        output.description = f"\n[{song['title']}]({song['source']})"
                        await ctx.response.send_message(embed=output)
                        await self.play_music(ctx)
                    else:
                        self.guildInfo[ctx.guild_id][2].append(song)
                        output.set_author(
                            name=COMMAND_PLAY_ADDED, icon_url=ICON_URL)
                        output.description = f"\n[{song['title']}]({song['source']})"
                        await ctx.response.send_message(embed=output)
                except Exception as ee:
                    logging.info(f"{ee}")
                    await ctx.response.send_message(f"{ee}")
            else:
                output.description = COMMAND_PLAY_ERROR
                output.color = Color.red()
                await ctx.response.send_message(embed=output, ephemeral=True)
        except Exception as e:
            logging.info(f"{e}")



    @app_commands.command(name=COMMAND_PLAYLIST_NAME, description=COMMAND_PLAYLIST_DESCRIPTION)
    async def command_playlist(self, ctx: discord.Interaction) -> None:
        """
        Command that displays playlist to the user
        """

        output = discord.Embed()
        output.set_author(name=COMMAND_PLAYLIST_CURRENT, icon_url=ICON_URL)
        try:
            if not self.guildInfo[ctx.guild_id] == None:
                if len(self.guildInfo[ctx.guild_id][2]) > 0:
                    output.description = ""
                    itt = 1
                    for song in self.guildInfo[ctx.guild_id][2]:
                        output.description += str(itt) + ". " + \
                            f"[{song['title']}]({song['source']})\n"
                        itt += 1
                    output.color = Color.green()
                    await ctx.response.send_message(embed=output)
                    return
            output.description = COMMAND_PLAYLIST_EMPTY
            output.color = Color.red()
            await ctx.response.send_message(embed=output, ephemeral=True)
            return
        except Exception:
            output.description = COMMAND_PLAYLIST_EMPTY
            output.color = Color.red()
            await ctx.response.send_message(embed=output, ephemeral=True)
            return
        


    @app_commands.command(name=COMMAND_SKIP_NAME, description=COMMAND_SKIP_DESCRIPTION)
    async def command_skip(self, ctx: discord.Interaction) -> None:
        """
        Command that skips currently playing song
        """
        
        output = discord.Embed()
        try:
            if self.guildInfo[ctx.guild_id][3]:
                ctx.guild.voice_client.stop()
                await self.play_music(ctx)
                output.color = Color.green()
                output.set_author(name=COMMAND_SKIP_SKIPPED, icon_url=ICON_URL)
                output.description = f"[{self.guildInfo[ctx.guild_id][5]['title']}]({self.guildInfo[ctx.guild_id][5]['source']})"
                await ctx.response.send_message(embed=output)
                return
            output.color = Color.red()
            output.description = COMMAND_SKIP_NOTRACK
            await ctx.response.send_message(embed=output, ephemeral=True)
        except Exception:
            output.color = Color.red()
            output.description = COMMAND_SKIP_NOTRACK
            await ctx.response.send_message(embed=output, ephemeral=True)



    @app_commands.command(name=COMMAND_CURRENTSONG_NAME, description=COMMAND_CURRENTSONG_DESCRIPTION)
    async def command_currentsong(self, ctx: discord.Interaction) -> None:
        """
        Command that displays currently playing song
        """

        output = discord.Embed()
        try:
            if self.guildInfo[ctx.guild_id][3]:
                output.set_author(
                    name=COMMAND_CURRENTSONG_CURRENT, icon_url=ICON_URL)
                output.description = f"[{self.guildInfo[ctx.guild_id][5]['title']}]({self.guildInfo[ctx.guild_id][5]['source']})"
                output.color = Color.green()
                await ctx.response.send_message(embed=output)
                return
            output.description = "No song is currently playing"
            output.color = Color.red()
            await ctx.response.send_message(embed=output, ephemeral=True)
        except Exception:
            output.description = "No song is currently playing"
            output.color = Color.red()
            await ctx.response.send_message(embed=output, ephemeral=True)



    @app_commands.command(name=COMMAND_PAUSE_NAME, description=COMMAND_PAUSE_DESCRIPTION)
    async def command_pause(self, ctx: discord.Interaction) -> None:
        """
        Command that pauses currently playing song
        """

        output = discord.Embed()
        try:
            if self.guildInfo[ctx.guild_id][3]:
                ctx.guild.voice_client.pause()
                output.color = Color.green()
                output.set_author(
                    name=f"{COMMAND_PAUSE_PAUSE}", icon_url=ICON_URL)
                await ctx.response.send_message(embed=output)
                return
            output.color = Color.red()
            output.description = COMMAND_PAUSE_ERROR
            await ctx.response.send_message(embed=output, ephemeral=True)
        except Exception:
            output.color = Color.red()
            output.description = COMMAND_PAUSE_ERROR
            await ctx.response.send_message(embed=output, ephemeral=True)



    @app_commands.command(name=COMMAND_RESUME_NAME, description=COMMAND_RESUME_DESCRIPTION)
    async def command_resume(self, ctx: discord.Interaction) -> None:
        """
        Command that resumes currently playing song
        """

        output = discord.Embed()
        if ctx.guild.voice_client.is_paused():
            ctx.guild.voice_client.resume()
            output.set_author(name=COMMAND_RESUME_RESUME, icon_url=ICON_URL)
            output.color = Color.green()
            await ctx.response.send_message(embed=output)
        else:
            output.description = COMMAND_RESUME_ERROR
            output.color = Color.red()
            await ctx.response.send_message(embed=output, ephemeral=True)



    @app_commands.command(name=COMMAND_CLEAR_NAME, description=COMMAND_CLEAR_DESCRIPTION)
    async def command_clear(self, ctx: discord.Interaction) -> None:
        """
        Command that clears the queue
        """
        
        output = discord.Embed()
        try:
            if len(self.guildInfo[ctx.guild_id][2]) > 0:
                self.guildInfo[ctx.guild_id][2] = []
                output.set_author(name=COMMAND_CLEAR_CLEAR, icon_url=ICON_URL)
                output.color = Color.green()
                await ctx.response.send_message(embed=output)
            else:
                output.description = COMMAND_CLEAR_ERROR
                output.color = Color.red()
                await ctx.response.send_message(embed=output, ephemeral=True)
        except Exception as e:
            logging.info(f"{e}")
            output.description = COMMAND_CLEAR_ERROR
            output.color = Color.red()
            await ctx.response.send_message(embed=output, ephemeral=True)



    @app_commands.command(name=COMMAND_STOP_NAME, description=COMMAND_STOP_DESCRIPTION)
    async def command_stop(self, ctx: discord.Interaction) -> None:
        """
        Command that stops the current queue and clears it
        """

        output = discord.Embed()
        try:
            if self.guildInfo[ctx.guild_id][3]:
                ctx.guild.voice_client.stop()
            if await self.disconnect(ctx):
                output.set_author(name=COMMAND_STOP_STOP, icon_url=ICON_URL)
                output.color = Color.green()
                await ctx.response.send_message(embed=output)
            else:
                output.description = COMMAND_STOP_ERROR
                output.color = Color.red()
                await ctx.response.send_message(embed=output, ephemeral=True)
        except Exception:
            output.description = COMMAND_STOP_ERROR
            output.color = Color.red()
            await ctx.response.send_message(embed=output, ephemeral=True)



    @app_commands.command(name=COMMAND_REMOVE_NAME, description=COMMAND_REMOVE_DESCRIPTION)
    @app_commands.describe(id=COMMAND_REMOVE_ID)
    async def command_remove(self, ctx: discord.Interaction, id: int) -> None:
        """
        Command that removes song from queue by id provided by playlist
        """

        output = discord.Embed()
        try:
            song = self.guildInfo[ctx.guild_id][2][id - 1]
            self.guildInfo[ctx.guild_id][2].pop(id-1)
            output.color = Color.green()
            output.set_author(name=COMMAND_REMOVE_REMOVED, icon_url=ICON_URL)
            output.description = f"[{song['title']}]({song['source']})"
            await ctx.response.send_message(embed=output)
        except Exception:
            output.color = Color.red()
            output.description = COMMAND_REMOVE_ERROR
            await ctx.response.send_message(embed=output, ephemeral=True)



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """
    
    await bot.add_cog(Music(bot))
