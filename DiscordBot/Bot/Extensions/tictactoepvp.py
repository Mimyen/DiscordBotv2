import discord
from discord.ext import commands
from discord import app_commands
from discord import Color
from ..Config.config import *
from PIL import Image, ImageFilter



class TicTacToePVP(commands.Cog):
    """
    TicTacToePVP extension lets user play a game of tic tac toe with another discord user
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes extension
        """

        self.bot = bot
        self.Game = {}
        self.View = {}
        self.Players = {}
        self.creator = self.BoardCreator()
    
    class BoardCreator:
        """
        BoardCreator makes an image of the game board
        """

        def __init__(self):
            """
            Initializes BoardCreator
            """

            # Set variables
            self.board_size = 424
            self.tile_size = 128
            self.spacing_size = 20

            self.path = BOARD_ASSETS_PATH
            self.savePath = BOARD_SAVE_PATH

            # Load images for empty space, X, O, and spacings
            self.empty_image = Image.open(f"{self.path}empty.png").resize((self.tile_size, self.tile_size))
            self.x_image = Image.open(f"{self.path}x.png").resize((self.tile_size, self.tile_size))
            self.o_image = Image.open(f"{self.path}o.png").resize((self.tile_size, self.tile_size))
            self.y_spacing = Image.open(f"{self.path}yspacing.png").resize((self.tile_size * 3 + self.spacing_size * 2, self.spacing_size))
            self.x_spacing1 = Image.open(f"{self.path}xspacing1.png").resize((self.spacing_size, self.tile_size))
            self.x_spacing2 = Image.open(f"{self.path}xspacing2.png").resize((self.spacing_size, self.tile_size))
            self.x_spacing3 = Image.open(f"{self.path}xspacing3.png").resize((self.spacing_size, self.tile_size))



        def create(self, ttoMap: list[int], name: str ="ttoboard") -> str:
            """
            Creates the image of the game using `ttoMap` and return name of the image `name`

            `ttoMap` is list of length 9 containing int values (either -1, 0 or 1)

            `name` is a string which is used to make a file containing the image ('name'.png)
            """

            # Creating the board
            tic_tac_toe_board = Image.new("RGBA", (self.board_size, self.board_size), color="white")

            # Addign elements
            for row in range(5):
                for col in range(5):
                    index = int(row / 2) * 3 + int(col / 2)
                    tile = ttoMap[index]
                    if row % 2 == 0 and col % 2 == 0:
                        if tile == 1:
                            tic_tac_toe_board.paste(self.x_image, (int(col / 2) * (self.tile_size + self.spacing_size), int(row / 2) * (self.tile_size + self.spacing_size)))
                        elif tile == -1:
                            tic_tac_toe_board.paste(self.o_image, (int(col / 2) * (self.tile_size + self.spacing_size), int(row / 2) * (self.tile_size + self.spacing_size)))
                        else:
                            tic_tac_toe_board.paste(self.empty_image, (int(col / 2) * (self.tile_size + self.spacing_size), int(row / 2) * (self.tile_size + self.spacing_size)))
                    else:
                        if row % 2 == 1 and col == 0:
                            tic_tac_toe_board.paste(self.y_spacing, (int(col / 2) * (self.tile_size + self.spacing_size), (int(row / 2) + 1) * (self.tile_size) + (int(row / 2)) * (self.spacing_size)))
                        elif row == 0:
                            tic_tac_toe_board.paste(self.x_spacing1, ((int(col / 2) + 1) * (self.tile_size) + (int(col / 2)) * (self.spacing_size), int(row / 2) * (self.tile_size + self.spacing_size)))
                        elif row == 2:
                            tic_tac_toe_board.paste(self.x_spacing3, ((int(col / 2) + 1) * (self.tile_size) + (int(col / 2)) * (self.spacing_size), int(row / 2) * (self.tile_size + self.spacing_size)))
                        elif row == 4:
                            tic_tac_toe_board.paste(self.x_spacing2, ((int(col / 2) + 1) * (self.tile_size) + (int(col / 2)) * (self.spacing_size), int(row / 2) * (self.tile_size + self.spacing_size)))

            # Antialiasing
            tic_tac_toe_board = tic_tac_toe_board.filter(ImageFilter.SHARPEN)

            # Saving image as file
            tic_tac_toe_board.save(f"{self.savePath}{name}.png")

            # Return path to the file
            return (f"{self.savePath}{name}.png")



    class TTTGame():
        """
        TTTGame is class representing the game itself
        """

        def __init__(self):
            """
            Initializes the class
            """
             
            self.markers = {
                -1: '⭕',
                0: '✖️',
                1: '❌',
            }

            # Player input:
            #   1  2  3
            #   4  5  6
            #   7  8  9
            # Real location n-1
            self.map = [
                0, 0, 0,
                0, 0, 0,
                0, 0, 0,
            ]

            self.moveId = 1
            self.isWon = 0

     

        def moveInput(self, mapId: int, isPlayer: bool = True) -> bool:
            """
            Method that makes the move by editing map

            `mapId` is integer in 1-9 range

            `isPlayer` is boolean value representing whether move is made by a Player (True) or a bot (False)
            """

            if mapId < 1 or mapId > 9:
                return False

            if isPlayer and self.map[mapId - 1] == 0:
                if self.moveId % 2 == 1:
                    self.map[mapId - 1] = 1
                else:
                    self.map[mapId - 1] = -1
                return True

            return False

        

        def handleButton(self, buttonId: int) -> tuple[bool, None | int]:
            """
            Method that handles player move which is made by using a button

            `buttonId` is integer representing id of button that was used
            """

            correctMove: bool = False

            if self.moveId <= 9:
                match buttonId:
                    case 1:
                        correctMove = self.moveInput(1)
                    case 2:
                        correctMove = self.moveInput(2)
                    case 3:
                        correctMove = self.moveInput(3)
                    case 4:
                        correctMove = self.moveInput(4)
                    case 5:
                        correctMove = self.moveInput(5)
                    case 6:
                        correctMove = self.moveInput(6)
                    case 7:
                        correctMove = self.moveInput(7)
                    case 8:
                        correctMove = self.moveInput(8)
                    case 9:
                        correctMove = self.moveInput(9)

            if correctMove:
                self.moveId += 1

            self.isWon = self.checkWin()

            return correctMove

        

        def checkWin(self) -> int:
            """
            Method that checks whether the game is won
            """

            for i in [0, 1, 2]:
                if self.map[i*3 + 0] == self.map[i*3 + 1] == self.map[i*3 + 2] != 0:
                    return self.map[i*3 + 0]

                if self.map[i] == self.map[i + 3] == self.map[i + 6] != 0:
                    return self.map[i]

            if self.map[0] == self.map[4] == self.map[8] != 0:
                return self.map[0]
            if self.map[2] == self.map[4] == self.map[6] != 0:
                return self.map[2]

            return 0

   

    class PVPGameView(discord.ui.View):
        """
        Class that creates a View containing buttons for a game
        """
        def __init__(self, tttReference):
            """
            Initializes the class
            """

            super().__init__()
            self.ref = tttReference

        
        
        async def action(self, ctx: discord.Interaction, btnId: int) -> None:
            """
            Method that is run after button is pressed

            `btnId` is integer representing id of a button
            """

            if self.ref.Players[ctx.message.id][(self.ref.Game[ctx.message.id][0].moveId - 1) % 2] != str(ctx.user.id):
                await ctx.response.defer(ephemeral=True)
                return

            savedKey = None
            correct = self.ref.Game[ctx.message.id][0].handleButton(btnId)

            if correct:
                self.children[btnId - 1].disabled = True

                if self.ref.Game[ctx.message.id][0].isWon == 0:
                    if self.ref.Game[ctx.message.id][0].moveId > 9:
                        await self.ref.update(ctx.message.id, self.ref.Game[ctx.message.id][1], winner="Tie")
                    else:
                        await self.ref.update(ctx.message.id, self.ref.Game[ctx.message.id][1])
                else:
                    await self.ref.update(ctx.message.id, self.ref.Game[ctx.message.id][1], winner=f"{self.ref.Players[ctx.message.id][(self.ref.Game[ctx.message.id][0].moveId) % 2]}")
                    savedKey = ctx.message.id

            if savedKey != None:
                self.ref.Game.pop(savedKey)
                self.ref.Players.pop(savedKey)
                self.ref.View.pop(savedKey)

            await ctx.response.defer(ephemeral=True)



        @discord.ui.button(label="1", style=discord.ButtonStyle.grey, row=0)
        async def button_1(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 1 press
            """
            await self.action(ctx, 1)

        @discord.ui.button(label="2", style=discord.ButtonStyle.grey, row=0)
        async def button_2(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 2 press
            """
            await self.action(ctx, 2)

        @discord.ui.button(label="3", style=discord.ButtonStyle.grey, row=0)
        async def button_3(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 3 press
            """
            await self.action(ctx, 3)

        @discord.ui.button(label="4", style=discord.ButtonStyle.grey, row=1)
        async def button_4(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 4 press
            """
            await self.action(ctx, 4)

        @discord.ui.button(label="5", style=discord.ButtonStyle.grey, row=1)
        async def button_5(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 5 press
            """
            await self.action(ctx, 5)

        @discord.ui.button(label="6", style=discord.ButtonStyle.grey, row=1)
        async def button_6(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 6 press
            """
            await self.action(ctx, 6)

        @discord.ui.button(label="7", style=discord.ButtonStyle.grey, row=2)
        async def button_7(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 7 press
            """
            await self.action(ctx, 7)

        @discord.ui.button(label="8", style=discord.ButtonStyle.grey, row=2)
        async def button_8(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 8 press
            """
            await self.action(ctx, 8)

        @discord.ui.button(label="9", style=discord.ButtonStyle.grey, row=2)
        async def button_9(self, ctx: discord.Interaction, button: discord.ui.Button):
            """
            Method that activates on button 9 press
            """
            await self.action(ctx, 9)

    

    async def update(self, key, message, winner: str = "") -> None:
        """
        Method that updates original bots message

        `key` is id of message that will be edited

        `message` is discord.Message class object containing message that is updated

        `winner` is str containing the name of the winner
        """

        output = discord.Embed()
        output.set_author(name="Tic Tac Toe PvP v1.0", icon_url=ICON_URL)
        output.description = ""
        output.color = Color.teal()

        fileName = self.creator.create(self.Game[key][0].map, f'{key}')
        file = discord.File(f"{fileName}", f"board.png")

        output.set_image(url=f"attachment://{file.filename}")

        if len(winner) > 0:

            if winner == "Tie":
                output.description += f"\n\nThis game ended in a tie!"
            else:
                output.description += f"\n\n<@{winner}> won the game!"

            await message.edit(embed=output, view=None, attachments=[file])
            return

        output.description += f"\n\n<@{self.Players[key][(self.Game[key][0].moveId - 1) % 2]}> turn!"
        await message.edit(embed=output, view=self.View[key], attachments=[file])

   

    @app_commands.command(name=COMMAND_CREATEGAMEPVP_NAME, description=COMMAND_CREATEGAMEPVP_DESCRIPTION)
    @app_commands.describe(player1=COMMAND_CREATEGAMEPVP_PLAYERONE, player2=COMMAND_CREATEGAMEPVP_PLAYERTWO)
    async def command_creategamepvp(self, ctx: discord.Interaction, player1: str, player2: str) -> None:
        """
        Command that creates a game of tic tac toe
        """

        output = discord.Embed()
        output.set_author(name="Tic Tac Toe PvP v1.0", icon_url=ICON_URL)
        output.color = Color.teal()
        output.description = ""

        await ctx.response.send_message(embed=output)
        message = await ctx.original_response()

        self.View[message.id] = self.PVPGameView(self)
        self.Game[message.id] = [self.TTTGame(), message]
        self.Players[message.id] = [player1.replace('<', '').replace(
            '@', '').replace('>', ''), player2.replace('<', '').replace('@', '').replace('>', '')]

        await self.update(message.id, message)



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """
    
    await bot.add_cog(TicTacToePVP(bot))
