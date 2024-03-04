import discord
import random
import logging
import os
from discord.ext import commands
from discord import app_commands
from discord import Color
from ..Config.config import *
from PIL import Image, ImageFilter


class TicTacToe(commands.Cog):
    """
    TicTacToe extension lets user play a game of tic tac toe with a bot
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes extension
        """

        self.bot = bot
        self.Game = {}
        self.View = {}
        self.Author = {}
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

        def __init__(self, playerStarts: bool = True, botDifficulty: int = 1):
            """
            Initializes the class

            `playerStarts` is boolean value used for choosing who starts (True - Player, False - Bot)

            `botDifficulty` is integer representing difficulty bot will be playing with (0 - Easy, 1 - Medium, 2 - Hard)
            """

            self.difficulty = botDifficulty

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

            if playerStarts:
                self.markerOffset = 1
            else:
                self.markerOffset = -1

            self.moveId = 1
            self.isWon = 0

            if not playerStarts:
                self.botMove()
                self.moveId += 1



        def moveInput(self, mapId: int, isPlayer: bool = True) -> bool:
            """
            Method that makes the move by editing map

            `mapId` is integer in 1-9 range

            `isPlayer` is boolean value representing whether move is made by a Player (True) or a bot (False)
            """

            if mapId < 1 or mapId > 9:
                return False

            if isPlayer and self.map[mapId - 1] == 0:
                self.map[mapId - 1] = 1 * self.markerOffset
                return True
            elif not isPlayer:
                self.map[mapId - 1] = (-1) * self.markerOffset
                return True

            return False



        def botMove(self) -> None | int:
            """
            Method that calculates next bots move
            """

            if self.difficulty == 0:

                if self.map[value := 1] == 0:
                    self.moveInput(2, isPlayer=False)

                elif self.map[value := 3] == 0:
                    self.moveInput(4, isPlayer=False)

                elif self.map[value := 5] == 0:
                    self.moveInput(6, isPlayer=False)

                elif self.map[value := 7] == 0:
                    self.moveInput(8, isPlayer=False)

                elif self.map[value := 0] == 0:
                    self.moveInput(1, isPlayer=False)

                elif self.map[value := 2] == 0:
                    self.moveInput(3, isPlayer=False)

                elif self.map[value := 6] == 0:
                    self.moveInput(7, isPlayer=False)

                elif self.map[value := 8] == 0:
                    self.moveInput(9, isPlayer=False)

                elif self.map[value := 4] == 0:
                    self.moveInput(5, isPlayer=False)

                return (value + 1)

            elif self.difficulty == 1:

                while not self.map[(value := random.randint(1, 9)) - 1] == 0:
                    pass

                self.moveInput(value, isPlayer=False)

                return value

            elif self.difficulty == 2:

                self.moveInput(value := self.moveSetup(), isPlayer=False)

                return value

            return None

        def moveSetup(self) -> int:
            """
            Method that initializes hard difficulty bots way of retreving next best move
            """
            
            botMove = self.markerOffset * (-1)
            moves = [1, 3, 9, 7]

            if self.moveId == 1:
                if random.randint(0, 1) == 1:
                    
                    return moves[random.randint(0, 3)]
                else:
                    return 5

            if self.moveId == 2:
                if self.map[4] == 0:
                    return 5
                else: 
                    return moves[random.randint(0,3)]
                
            if self.moveId == 3:
                if self.map[4] == botMove:
                    checker = True
                    while checker:
                        if self.map[index := ((moves[rand := random.randint(0,3)]) - 1)] == 0 and self.map[index] == 0:
                            checker = False
                            return index + 1
                else:
                    for i, pos in enumerate(self.map):
                            if pos == botMove:
                                botLastMove = i + 1

                    for i, move in enumerate(moves):
                        if botLastMove == move:
                            index = i

                    if self.map[4] == (-1) * botMove:
                        return moves[index - 2]

                    else:
                        if self.map[int(moves[index - 1] + ((moves[index] - moves[index - 1])/2)) - 1] == 0 and self.map[moves[index - 1] - 1] == 0: return moves[index - 1]
                        else: return moves[index - 3]

            if self.moveId == 4:
                index = None
                for i, pos in enumerate(self.map):
                    if pos == -botMove and (i + 1) in moves:
                        index = i
                        break
                
                if not index is None:
                    saved = 0
                    for i, move in enumerate(moves):
                        if index + 1 == move:
                            saved = i
                    
                    if self.map[moves[saved] - 1] == self.map[moves[saved - 2] - 1] == -botMove:
                        return [2,4,6,8][random.randint(0,3)]
                    
            if self.moveId == 9:
                for i, pos in enumerate(self.map):
                    if pos == 0: return i + 1

            moves = []

            for i, pos in enumerate(self.map):
                if pos == 0:
                    ttomap = self.map[:]
                    ttomap[i] = botMove
                    moves.append([i, self.moveFinder(ttomap[:], botMove, 1, 11 - self.moveId)])

            m = -999999999999
            for obj in moves:
                if obj[1] > m:
                    m = obj[1]
                    index = obj[0]
            
            return index + 1
        


        def moveFinder(self, mmap: list[int], botMove: int, offset: int, depth: int) -> int:
            """
            Method that calculates value that represents how good a move is (higher - better)

            `mmap` is list containing edited map with a move made

            `botMove` is integer value that bot will put into map whenever it makes a move

            `offset` is integer value tells us whether it's bots move to make

            `depth` is integer value that tells us how many moves in function is called (lower - deeper)
            """

            if self.checkWin(mmap) == -1: return 1 * depth ** 4
            elif self.checkWin(mmap) == 1: return -10 * depth ** 6

            zeros = 0
            for pos in mmap:
                if pos == 0: zeros += 1

            if zeros == 0: return 0

            outcome = 0
        
            for i, pos in enumerate(mmap):
                if pos == 0:
                    ttomap = mmap[:]
                    ttomap[i] = botMove * offset * -1
                    outcome += self.moveFinder(ttomap[:], botMove, -offset, depth - 1)

            return outcome
        


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

            value = None

            if self.moveId <= 9 and correctMove and self.isWon == 0:
                value = self.botMove()
                self.moveId += 1

            self.isWon = self.checkWin()

            return (correctMove, value)




        def checkWin(self, mmap: None | list = None) -> int:
            """
            Method that checks whether the game is won

            `mmap` is list of lenght 9 containing integer values (-1, 0 or 1)
            """

            if mmap is None:
                for i in [0, 1, 2]:
                    if self.map[i*3 + 0] == self.map[i*3 + 1] == self.map[i*3 + 2] != 0:
                        return self.map[i*3 + 0] * self.markerOffset

                    if self.map[i] == self.map[i + 3] == self.map[i + 6] != 0:
                        return self.map[i] * self.markerOffset

                if self.map[0] == self.map[4] == self.map[8] != 0:
                    return self.map[0] * self.markerOffset
                if self.map[2] == self.map[4] == self.map[6] != 0:
                    return self.map[2] * self.markerOffset
            else:
                for i in [0, 1, 2]:
                    if mmap[i*3 + 0] == mmap[i*3 + 1] == mmap[i*3 + 2] != 0:
                        return mmap[i*3 + 0] * self.markerOffset

                    if mmap[i] == mmap[i + 3] == mmap[i + 6] != 0:
                        return mmap[i] * self.markerOffset

                if mmap[0] == mmap[4] == mmap[8] != 0:
                    return mmap[0] * self.markerOffset
                if mmap[2] == mmap[4] == mmap[6] != 0:
                    return mmap[2] * self.markerOffset

            return 0




    class GameView(discord.ui.View):
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

            if self.ref.Author[ctx.message.id] != ctx.user.id:
                await ctx.response.defer(ephemeral=True)
                return

            isWon = 0
            savedKey = None
            correct, value = self.ref.Game[ctx.message.id][0].handleButton(
                btnId)

            if correct:
                self.children[btnId - 1].disabled = True

                if value is not None:
                    self.children[value - 1].disabled = True

                if value is None:
                    for i in range(9):
                        self.children[i].disabled = True

                if (isWon := self.ref.Game[ctx.message.id][0].isWon) == 0:
                    if value is None:
                        await self.ref.update(ctx.message.id, self.ref.Game[ctx.message.id][1], winner="Tie")
                    else:
                        await self.ref.update(ctx.message.id, self.ref.Game[ctx.message.id][1])
                else:

                    if isWon == 1:
                        await self.ref.update(ctx.message.id, self.ref.Game[ctx.message.id][1], winner="Player")
                    if isWon == -1:
                        await self.ref.update(ctx.message.id, self.ref.Game[ctx.message.id][1], winner="Bot")
                    savedKey = ctx.message.id

            if savedKey != None:
                self.ref.Game.pop(savedKey)

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



    async def update(self, key: int, message: discord.Message, winner: str = "") -> None:
        """
        Method that updates original bots message

        `key` is id of message that will be edited

        `message` is discord.Message class object containing message that is updated

        `winner` is str containing the name of the winner
        """

        output = discord.Embed()
        output.set_author(name="Tic Tac Toe v1.1", icon_url=ICON_URL)
        output.description = ""
        output.color = Color.teal()

        fileName = self.creator.create(self.Game[key][0].map, f'{key}')
        file = discord.File(f"{fileName}", f"board.png")

        output.set_image(url=f"attachment://{file.filename}")

        if len(winner) > 0:

            if winner == "Tie":
                output.description += f"\n\nThis game ended in a tie!"
            else:
                output.description += f"\n\n{winner} won the game!"

            await message.edit(embed=output, view=None, attachments=[file])
            return

        await message.edit(embed=output, view=self.View[key], attachments=[file])



    @app_commands.command(name=COMMAND_CREATEGAME_NAME, description=COMMAND_CREATEGAME_DESCRIPTION)
    @app_commands.describe(starts=COMMAND_CREATEGAME_PLAYERSTARTS, difficulty=COMMAND_CREATEGAME_DIFFICULTY)
    @app_commands.choices(starts=[
        app_commands.Choice(name="Player", value=1),
        app_commands.Choice(name="Bot", value=0),
    ],
        difficulty=[
        app_commands.Choice(name="Easy", value=0),
        app_commands.Choice(name="Medium", value=1),
        app_commands.Choice(name="Hard", value=2)
    ])
    async def command_creategame(self, ctx: discord.Interaction, starts: app_commands.Choice[int], difficulty: app_commands.Choice[int] = None) -> None:
        """
        Command that creates a game of tic tac toe
        """

        if difficulty is None:
            difficulty = app_commands.Choice(name='Medium', value=1)
        logging.info(f"New Game: {difficulty.name}")
        output = discord.Embed()
        output.set_author(name="Tic Tac Toe v1.1", icon_url=ICON_URL)
        output.color = Color.teal()
        output.description = ""

        await ctx.response.send_message(embed=output)
        message = await ctx.original_response()

        self.View[message.id] = self.GameView(self)
        self.Game[message.id] = [self.TTTGame(bool(starts.value), difficulty.value), message]
        self.Author[message.id] = ctx.user.id

        if not bool(starts.value): 
            for i, pos in enumerate(self.Game[message.id][0].map):
                if pos != 0:
                    index = i
            
            self.View[message.id].children[index].disabled = True

        await self.update(message.id, message)



async def setup(bot):
    """
    Function that is run whenever bot tries to add extension to itself
    """
    
    await bot.add_cog(TicTacToe(bot))
