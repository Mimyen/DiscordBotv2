
    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user) -> None:
    #     message = reaction.message
    #     isWon = 0
    #     savedKey = None
    #     for key in self.Game:
    #         if self.Game[key][1] == message and user != self.bot.user:
    #             if self.Game[key][0].handleEmoji(reaction.emoji):
    #                 if (isWon := self.Game[key][0].isWon) == 0:
    #                     await self.update(key, message)
    #                 else:
    #                     if isWon == 1: await self.update(key, message, winner="Player")
    #                     if isWon == -1: await self.update(key, message, winner="Bot")
    #                     savedKey = key
    #             await reaction.remove(user=user)
    #     if savedKey != None:
    #         await message.clear_reactions()
    #         self.Game.pop(savedKey)
