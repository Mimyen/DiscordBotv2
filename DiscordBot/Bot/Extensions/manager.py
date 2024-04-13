import discord
import random
import datetime
import logging
import asyncio
import json
import os
import re
import websockets
from flask import Flask, request, current_app
from flask_restx import Api, Resource, fields
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from discord.ext import commands
from discord import app_commands
from ..Config.config import *
from discord import Color

__version__ = "0.0.1"


class Manager(commands.Cog):
    """
    Extansion that lets owner of the bot control it in desktop application
    """

    def __init__(self, bot: commands.Bot, password: str = MANAGER_PASSWORD):
        """
        Initializing the extansion (cog)

        To change the password you need to edit config file
        """
        logging.getLogger("manager")
        self.bot = bot

        self.authorizedUsers = []
        self.tokens = []
        self.password = password

        self.managerGetChatWebsockets: dict[str, websockets.WebSocketServerProtocol] = {}

        with open("Temp/admin/data", 'r') as file:
            for line in file:
                self.authorizedUsers.append(line.strip('\n'))

        # logging.info(self.authorizedUsers)

        self.bot.loop.create_task(self.__startWebSocketServer())

        self.flask_app = Flask(__name__)
        self.api = Api(self.flask_app, version='0.1', title='DiscordBOT Manager API',
                       description='API ', doc=MANAGER_DOSC_ROUTE)
        self.setup_api()
        self.flask_app.config["bot"] = self.bot
        self.flask_app.config["extension"] = self
        self.bot.loop.create_task(self.__startHTTPServer())

        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        for key in self.managerGetChatWebsockets:
            if key == str(message.channel.id):
                await self.managerGetChatWebsockets[key].send(message.content)


    def setup_api(self):
        """Sets up the Flask-RESTx API."""
        ns = self.api.namespace('managerapi', description='Operations on the bot')

        color_model = ns.model('ColorModel', {
            'r': fields.String(required=False, description='RGB value for red'),
            'g': fields.String(required=False, description='RGB value for green'),
            'b': fields.String(required=False, description='RGB value for blue')
        })

        # Define the model for the 'author' part of the message
        author_model = ns.model('AuthorModel', {
            'name': fields.String(required=False, description='Name of the author for embedded format'),
            'icon': fields.String(required=False, description='Icon for the author for embedded format (link)')
        })

        # Define the main message model that includes the nested models
        message_model = ns.model('MessageModel', {
            'id': fields.String(required=True, description='Login that has been authenticated'),
            'token': fields.String(required=True, description='Token received when authenticating'),
            'message': fields.String(required=True, description='Message that you want to send'),
            'server_id': fields.String(required=True, description='Discord server id that you want to send message to'),
            'channel_id': fields.String(required=True, description='Discord channel id that you want to send message to'),
            'embedded': fields.String(required=True, description='Indicates if the message should be embedded'),
            'color': fields.Nested(color_model, required=False, description='Color information for embedded format'),
            'author': fields.Nested(author_model, required=False, description='Author information for embedded format')
        })

        server_data_model = self.api.model(
                    'GetServerData JSON', 
                    {
                        'id': fields.String(required=True, description='Login that has been authenticated'),
                        'token': fields.String(required=True, description='Token recieved when authenticating'),
                        'server_id': fields.String(required=True, description='Discord server id that you want to recieve text channels from') 
                    }
                )


        @ns.route('/sendmessage')
        class Message(Resource):

            @ns.expect(
                message_model, 
                validate=True
            )


            def post(self):
                """Send a message"""
                bot: commands.bot = current_app.config["bot"]
                extension: Manager = current_app.config["extension"]

                data = self.api.payload

                async def sendMessage(bot: commands.bot, data: dict, embed: discord.Embed | None = None) -> None:
                    if embed is not None:
                        await bot.get_guild(int(data['server_id'])).get_channel(int(data['channel_id'])).send(embed=embed)
                    else:
                        await bot.get_guild(int(data['server_id'])).get_channel(int(data['channel_id'])).send(data['message'])
                
                if data['id'] in extension.authorizedUsers and data['token'] in extension.tokens:
                    if data['embedded'] == 'true':
                        embed = discord.Embed()

                        embed.description = data['message']

                        try:
                            if data['color']:
                                embed.color = Color.from_rgb(int(data['color']['r']), int(data['color']['g']), int(data['color']['b']))
                        except:
                            pass

                        try:
                            if data['author']:
                                embed.set_author(name=data['author']['name'], icon_url=data['author']['icon'])
                        except:
                            pass

                        bot.loop.create_task(sendMessage(bot, data, embed))

                    else:
                        bot.loop.create_task(sendMessage(bot, data))

                return {'message': 'Message sent'}, 200
            

        @ns.route('/authenticate')
        class Authenticate(Resource):

            @ns.expect(
                self.api.model(
                    'Authentication JSON', 
                    {
                        'id': fields.String(required=True, description='Login to the manager'),
                        'password': fields.String(required=True, description='Password to the manager')
                    }
                ), 
                validate=True
            )

            def post(self):
                """Authenticate"""
                bot: commands.bot = current_app.config["bot"]
                extension: Manager = current_app.config["extension"]

                data = self.api.payload
                logging.info(f"Received message: {data}")

                token = ""
                code = 401
                output = {'error': 'Unauthorized access'}
                if data['id'] in extension.authorizedUsers and extension.authenticate(data['password']):
                    token = str(random.randint(10000, 99999))
                    extension.tokens.append(token)
                    output.pop('error')
                    output['token'] = token
                    code = 200
                
                logging.info(extension.tokens)
                
                return output, code


        @ns.route('/getservers')
        class GetServers(Resource):

            @ns.expect(
                self.api.model(
                    'GetSevers JSON', 
                    {
                        'id': fields.String(required=True, description='Login that has been authenticated'),
                        'token': fields.String(required=True, description='Token recieved when authenticating')
                    }
                ), 
                validate=True
            )

            def get(self):
                """Get servers bot is connected to"""
                bot: commands.bot = current_app.config["bot"]
                extension: Manager = current_app.config["extension"]

                data = self.api.payload
                logging.info(f"Received message: {data}")

                code = 401
                output = {'error': 'Unauthorized access'}

                if data['id'] in extension.authorizedUsers and data['token'] in extension.tokens:
                    output.pop('error')
                    guilds = bot.guilds

                    for guild in guilds:
                        output[str(guild.id)] = guild.name

                    code = 200
                
                return output, code
            

        @ns.route('/gettextchannels')
        class GetTextChannels(Resource):

            @ns.expect(
                server_data_model, 
                validate=True
            )

            def get(self):
                """Get text channels in the discord server"""
                bot: commands.bot = current_app.config["bot"]
                extension: Manager = current_app.config["extension"]

                data = self.api.payload

                code = 401
                output = {'error': 'Unauthorized access'}

                if data['id'] in extension.authorizedUsers and data['token'] in extension.tokens:
                    output.pop('error')
                    guild = bot.get_guild(int(data['server_id']))

                    for channel in guild.text_channels:
                        if channel.category is not None:
                            output[str(channel.id)] = f"{channel.category.name}: {channel.name}"
                        else:
                            output[str(channel.id)] = f"{channel.name}"

                    code = 200

                output = extension.encodeJSON(output)

                return output, code


        @ns.route('/getusers')
        class GetUsers(Resource):

            @ns.expect(
                server_data_model, 
                validate=True
            )

            def get(self):
                """Get members of a discord server"""
                bot: commands.bot = current_app.config["bot"]
                extension: Manager = current_app.config["extension"]

                async def getUsers(bot: commands.bot, data: dict) -> dict:
                    output = {}
                    async for member in bot.get_guild(int(data['server_id'])).fetch_members(limit=None):
                        if member.nick is not None:
                            output[str(member.id)] = [member.name, member.nick]
                            output[str(member.id)][1] = output[str(member.id)][1].replace('"', '?.quote?.')
                        else:
                            output[str(member.id)] = [member.name, ""]
                    return output

                data = self.api.payload

                code = 401
                output = {'error': 'Unauthorized access'}

                if data['id'] in extension.authorizedUsers and data['token'] in extension.tokens:
                    output.pop('error')

                    future = asyncio.run_coroutine_threadsafe(getUsers(bot, data), bot.loop)
                    try:
                        output = future.result(timeout=10)  # Adjust the timeout as necessary
                        code = 200
                        logging.info(future)
                    except asyncio.TimeoutError:
                        output = {'error': 'Timeout while fetching members'}
                        code = 504
                    code = 200

                output = extension.encodeJSON(output)

                return output, code
            

        @ns.route('/banuser')
        class BanUser(Resource):

            @ns.expect(
                self.api.model(
                    'UserManagement JSON', 
                    {
                        'id': fields.String(required=True, description='Login that has been authenticated'),
                        'token': fields.String(required=True, description='Token recieved when authenticating'),
                        'server_id': fields.String(required=True, description='Server from which you want to ban the user'),
                        'user_id': fields.String(required=True, description='Id of the user'),
                        'reason': fields.String(required=False, description='Reason for the action')
                    }
                ), 
                validate=True
            )

            def post(self):
                """Ban user on discord server"""
                bot: commands.bot = current_app.config["bot"]
                extension: Manager = current_app.config["extension"]

                async def banUser(bot: commands.bot, data: dict, reason: str = "Kicked by bot!") -> None:
                    await bot.get_guild(int(data['server_id'])).get_member(int(data['user_id'])).ban(reason=reason)

                data = self.api.payload

                code = 401
                output = {'error': 'Unauthorized access'}

                if data['id'] in extension.authorizedUsers and data['token'] in extension.tokens:
                    output.pop('error')
                    
                    try:
                        if data['reason'] is not None:
                            bot.loop.create_task(banUser(bot, data, data['reason']))
                    except:
                        bot.loop.create_task(banUser(bot, data))

                    output = {'status': 'success'}
                    
                    code = 200

                return output, code


        @ns.route('/kick')
        class KickUser(Resource):

            @ns.expect(
                self.api.model(
                    'UserManagement JSON', 
                    {
                        'id': fields.String(required=True, description='Login that has been authenticated'),
                        'token': fields.String(required=True, description='Token recieved when authenticating'),
                        'server_id': fields.String(required=True, description='Server from which you want to ban the user'),
                        'user_id': fields.String(required=True, description='Id of the user'),
                        'reason': fields.String(required=False, description='Reason for the action')
                    }
                ), 
                validate=True
            )

            def post(self):
                """Kick user from a discord server"""
                bot: commands.bot = current_app.config["bot"]
                extension: Manager = current_app.config["extension"]

                async def kickUser(bot: commands.bot, data: dict, reason: str = "Kicked by bot!") -> None:
                    await bot.get_guild(int(data['server_id'])).get_member(int(data['user_id'])).kick(reason=reason)

                data = self.api.payload

                code = 401
                output = {'error': 'Unauthorized access'}

                if data['id'] in extension.authorizedUsers and data['token'] in extension.tokens:
                    output.pop('error')
                    
                    try:
                        if data['reason'] is not None:
                            bot.loop.create_task(kickUser(bot, data, data['reason']))
                    except:
                        bot.loop.create_task(kickUser(bot, data))
                        
                    output = {'status': 'success'}
                    
                    code = 200

                return output, code                    



    async def __handleSocket(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        """
        Inner method that is handling socket calls made by ManagerApp

        Received data should consist of json message that has 'message'
        containing name of the function that will be called

        This method is called whenever server receives a socket
        """
        async def OnError(websocket: websockets.WebSocketServerProtocol, logger: logging.Logger) -> None:
            #await websocket.send(json.dumps({'error': 'Internal server error'}))
            logger.error('Error occured, closing websocket')
            await websocket.close(code=1001, reason="Going away")
            await websocket.close_connection()

        logger = logging.getLogger('manager.WSServer')
        logger.info(f'Connection established on ws://{MANAGER_IP}:{MANAGER_WEBSOCKET_PORT}{path}')

        if path == '/getchat':
            logger.info(f'Socket connected to ws://{MANAGER_IP}:{MANAGER_WEBSOCKET_PORT}/getchat')
            logger = logging.getLogger('manager.WSServer.getchat')
            try:
                message = await websocket.recv()
                logger.info(f"Message recieved: {message}")

                jsonData = json.loads(message)
                channel_id = jsonData['channel_id']

                self.managerGetChatWebsockets[channel_id] = websocket

                while True:
                    message = await websocket.recv()
                    logger.info(f"Message recieved: {message}")

                    # Dispatch other messages here

            except:
                if channel_id is not None: self.managerGetChatWebsockets.pop(channel_id)
                await OnError(websocket, logger)
        
        else:
            logger.error(f'Connection dismissed, path is not supported')
            await websocket.send(json.dumps({'error': 'No such path is supported'}))
            await websocket.close(code=1001, reason="Going away")
            await websocket.close_connection()



    async def __startWebSocketServer(self) -> None:
        """
        Inner method that starts the server and sets up the socket handler

        To change ip and port, you need to change values in config
        """
        logging.getLogger('websockets').setLevel(logging.CRITICAL)
        logger = logging.getLogger('manager.WSServer')
    
        try:
            server = await websockets.serve(self.__handleSocket, MANAGER_IP, MANAGER_WEBSOCKET_PORT)
            logger.info(f'Server started on >> ws://{MANAGER_IP}:{MANAGER_WEBSOCKET_PORT}')

            await server.wait_closed()
        except Exception as e:
            logger.error(f'Error occured while starting Websocket Server: {e}')

    async def __startHTTPServer(self) -> None:
        # Setup aiohttp web app to run Flask app with aiohttp-wsgi
        app = web.Application()
        wsgi_handler = WSGIHandler(self.flask_app)
        app.router.add_route('*', '/{path_info:.*}', wsgi_handler)
        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, MANAGER_IP, MANAGER_HTTP_PORT)

        logger = logging.getLogger("manager.HTTPServer")
        logger.info(f"Server started on >> http://{MANAGER_IP}:{MANAGER_HTTP_PORT}/")
        logger.info(f"Documentation on >> http://{MANAGER_IP}:{MANAGER_HTTP_PORT}{MANAGER_DOSC_ROUTE}")
        
        await site.start()

    async def __authorize(self, password: str) -> bool:
        """
        Inner method that authorizes user

        This method is called inside handleSocket method 
        """

        if password == self.password:
            return True
        
        return False

    def authenticate(self, password: str) -> bool:
        """
        Inner method that authorizes user

        This method is called inside handleSocket method 
        """

        if password == self.password:
            return True
        
        return False
    
    def encodeJSON(self, jsonMSG: any) -> any:
        """Clears string from emotes and unwanted characters and encodes it"""
        response = json.dumps(jsonMSG)

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
        response = response.replace('?.quote?.', '\\"')
        response = response.encode()
        # logging.info(response)
        return json.loads(response)

async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """

    await bot.add_cog(Manager(bot))