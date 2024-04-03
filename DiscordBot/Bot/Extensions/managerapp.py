import discord
import random
import datetime
import logging
import socket
import asyncio
import json
import os
import re
from discord.ext import commands
from discord import app_commands
from ..Config.config import *
from discord import Color

__version__ = "0.0.1"


class ManagerApp(commands.Cog):
    """
    Extansion that lets owner of the bot control it in desktop application
    """

    def __init__(self, bot: commands.Bot, password: str = MANAGER_PASSWORD):
        """
        Initializing the extansion (cog)

        To change the password you need to edit config file
        """
        self.bot = bot

        self.authorizedUsers = []
        self.tokens = []
        self.password = password

        with open("Temp/admin/data", 'r') as file:
            for line in file:
                self.authorizedUsers.append(line.strip('\n'))

        logging.info(self.authorizedUsers)

        self.bot.loop.create_task(self.__startServer())
        #self.bot.loop.create_task(self.__consoleLoop())

    async def __consoleLoop(self):
        """
        Inner method that creates loop used in console for adding and showing admin ids
        """

        while True:
            logging.info("Waiting for input...")
            
            userInput = input(">>> ")

         
            if 'load' in userInput or 'refresh' in userInput:
                self.authorizedUsers = []

                with open("Temp/admin/data", 'r') as file:
                    for line in file:
                        self.authorizedUsers.append(line.strip('\n'))

                logging.info(self.data)

            elif 'add' in userInput:
                try:
                    userId = userInput.split(' ')[1]

                    with open("Temp/admin/data", 'a') as file:
                        file.write(f"{userId}\n")

                except:
                    logging.error("Error with adding new admin")

            elif 'close' in userInput:
                break




    async def __handleSocket(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        Inner method that is handling socket calls made by ManagerApp

        Received data should consist of json message that has 'message'
        containing name of the function that will be called

        This method is called whenever server receives a socket
        """

        try:
            response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_CALL}

            try:
                data = await reader.read(4096)
                # logging.info(data)
                message = data.decode('utf-8')
            except Exception as e:
                logging.error(f"Error reading data: {e}")

            try:
                jsonData = json.loads(message)
            except Exception as e:
                logging.error(f"Error decoding JSON: {e}")
                response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INVALID_JSON}

            try:
                if jsonData['id'] in self.authorizedUsers:
                    try:
                        if jsonData['token'] in self.tokens:
                            # Here are described socket calls
                            match jsonData[MANAGER_RESPONSE_MESSAGE]:
                                # Whenever entering this switch, user is already authorized
                                case 'authorize':
                                    try:
                                        if await self.__authorize(jsonData['password']):
                                            token = str(random.randint(10000, 99999))
                                            response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_AUTHORIZED, MANAGER_RESPONSE_OUTPUT: f"Welcome to Mimyen Bot Manager API {__version__}v", MANAGER_RESPONSE_TOKEN: token}
                                            self.tokens.append(token)
                                        else:
                                            response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_PASSWORD}
                                    except:
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_AUTH_DATA}
                                
                                # Returns all servers bot is connected to
                                case 'getservers':
                                    guilds = self.bot.guilds

                                    response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_CORRECT, MANAGER_RESPONSE_OUTPUT: {}}

                                    for guild in guilds:
                                        response_data[MANAGER_RESPONSE_OUTPUT][guild.id] = guild.name

                                # Returns all channels in a guild
                                case 'gettextchannels':
                                    try:
                                        guildId = int(jsonData['guild_id'])
                                        guild = self.bot.get_guild(guildId)

                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_CORRECT, MANAGER_RESPONSE_OUTPUT: {}}                            

                                        for channel in guild.text_channels:
                                            if channel.category is not None:
                                                response_data[MANAGER_RESPONSE_OUTPUT][channel.id] = f"{channel.category.name}: {channel.name}"
                                            else:
                                                response_data[MANAGER_RESPONSE_OUTPUT][channel.id] = f"{channel.name}"
                                    except:
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_GUILD_ID}

                                # Sends message in a channel
                                case 'send_message':
                                    try:
                                        try:
                                            if jsonData['embedded'] == 'true':
                                                embed = discord.Embed()

                                                embed.description = jsonData['input']
                                                
                                                try:
                                                    if jsonData['color']:
                                                        embed.color = Color.from_rgb(int(jsonData['color']['r']), int(jsonData['color']['g']), int(jsonData['color']['b']))
                                                except:
                                                    pass

                                                try:
                                                    if jsonData['author'] and jsonData['icon']:
                                                        embed.set_author(name=jsonData['author'], icon_url=jsonData['icon'])
                                                except:
                                                    pass

                                                await self.bot.get_guild(int(jsonData['guild_id'])).get_channel(int(jsonData['channel_id'])).send(embed=embed)
                                        except Exception as e:
                                            await self.bot.get_guild(int(jsonData['guild_id'])).get_channel(int(jsonData['channel_id'])).send(jsonData['input'])

                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_CORRECT, MANAGER_RESPONSE_OUTPUT: MANAGER_RESPONSE_SEND_MESSAGE_SENT} 
                                    except:
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_SEND_MESSAGE_ERROR}

                                # Returns all members of a guild
                                case 'getusers':
                                    try: 
                                        if jsonData['guild_id']:

                                            response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_CORRECT, MANAGER_RESPONSE_OUTPUT: {}}    

                                            async for member in self.bot.get_guild(int(jsonData['guild_id'])).fetch_members(limit=None):
                                                response_data[MANAGER_RESPONSE_OUTPUT][member.id] = member.name

                                    except Exception as e:
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_GUILD_ID}

                                # Returns all members of a guild
                                case 'getcogs':
                                    try: 
                                        pass

                                    except Exception as e:
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR}

                        else:
                            if jsonData[MANAGER_RESPONSE_MESSAGE] == 'authorize':
                                try:
                                    if await self.__authorize(jsonData['password']):
                                        token = str(random.randint(10000, 99999))
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_AUTHORIZED, MANAGER_RESPONSE_OUTPUT: f"Welcome to Mimyen Bot Manager {__version__}v", MANAGER_RESPONSE_TOKEN: token}
                                        self.tokens.append(token)
                                        logging.info(f"{self.tokens}")
                                    else:
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_PASSWORD}
                                except:
                                    response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_AUTH_DATA}
                    except:
                        if jsonData[MANAGER_RESPONSE_MESSAGE] == 'authorize':
                                try:
                                    if await self.__authorize(jsonData['password']):
                                        token = str(random.randint(10000, 99999))
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_AUTHORIZED, MANAGER_RESPONSE_OUTPUT: f"Welcome to Mimyen Bot Manager {__version__}v", MANAGER_RESPONSE_TOKEN: token}
                                        self.tokens.append(token)
                                        logging.info(f"{self.tokens}")
                                    else:
                                        response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_PASSWORD}
                                except:
                                    response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_INCORRECT_AUTH_DATA}
                else:
                    # If user is not already authorized, if sent socket is for authorization, trying to authorize the user
                    response_data = {MANAGER_RESPONSE: MANAGER_RESPONSE_ERROR, MANAGER_RESPONSE_MESSAGE: MANAGER_RESPONSE_NO_ACCESS}
            except Exception as e:
                logging.error(f"{e}")

            # Parse the JSON message
            try:
                # Prepare a JSON response
                response = json.dumps(response_data)

                response = response.encode('utf-16', 'surrogatepass').decode('utf-16')

                emoji_pattern = re.compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                        u"\U0001F000-\U0001F02F"  # Mahjong Tiles
                        u"\U0001F0A0-\U0001F0FF"  # Playing Cards
                        u"\U00002328"
                                        "]+", flags=re.UNICODE)
                
                decoded_string = response.encode().decode('unicode-escape')
                buffer = decoded_string.encode('utf-16', 'surrogatepass').decode('utf-16')
                response = emoji_pattern.sub(r'', buffer)

                # Send the JSON response back to the C++ client
                # logging.info(response.encode('utf-8'))
                writer.write(response.encode('utf-8'))
                await writer.drain()

            except json.JSONDecodeError:
                logging.error("Invalid JSON received")

        except Exception as ee:
            logging.error(f"An error occured in __handleSocket: {ee}")

        finally:
            writer.close()

        

    async def __startServer(self) -> None:
        """
        Inner method that starts the server and sets up the socket handler

        To change ip and port, you need to change values in config
        """
        server = await asyncio.start_server(self.__handleSocket, MANAGER_IP, MANAGER_PORT)

        async with server:
            await server.serve_forever()



    async def __authorize(self, password: str) -> bool:
        """
        Inner method that authorizes user

        This method is called inside handleSocket method 
        """

        if password == self.password:
            return True
        
        return False

    

async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """

    await bot.add_cog(ManagerApp(bot))