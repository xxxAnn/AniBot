import discord
from discord.ext import commands
import random

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kill(self, ctx, arg):
        await ctx.send(arg + " is dead")

    @commands.command()
    async def suicide(self, ctx):
        await ctx.send("https://www.mext.go.jp/a_menu/shotou/seitoshidou/1302907.htm")

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

    @commands.command(pass_context=True)
    async def pfp(self, ctx, *user: discord.Member):
        r = False
        if not user:
            user = ctx.message.author
            r = True
        if not r:
            user = user[0]
        await ctx.send(user.avatar_url)

    @commands.command(pass_context=True)
    async def love(self, ctx, *tuple):
        if len(tuple) > 1:
            if tuple[0] == "Xuning" and tuple[1] == "Nancy":
                await ctx.send("100" + "% Compatible")
            else:
                await ctx.send(str(random.randint(0, 100)) + "% Compatible")
        else:
            await ctx.send(str(random.randint(0,100)) + "% Compatible")


def setup(bot):
    bot.add_cog(Fun(bot))
