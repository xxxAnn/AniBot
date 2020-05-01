import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def emotify(self, ctx, *, arg):
        arg = str.lower(arg)
        x = ""
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                    "u",
                    "v", "w", "x", "y", "z"]
        for i in str(arg):
            if i == "":
                x = x + " "
            if i in alphabet:
                i = ":regional_indicator_" + i + ":"
                x = x + " " + i
        await ctx.send(x)


def setup(bot):
    bot.add_cog(Fun(bot))