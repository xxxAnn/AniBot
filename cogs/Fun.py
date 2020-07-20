import discord
from discord.ext import commands
import random
from Libraries.Library import get_guild_language, Pages, command_activated
import time
import inspect

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kill(self, ctx, arg):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        await ctx.send(arg + " is dead")

    @commands.command()
    async def suicide(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        await ctx.send("https://www.mext.go.jp/a_menu/shotou/seitoshidou/1302907.htm")

    @commands.command()
    async def emotify(self, ctx, *, arg):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
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
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        r = False
        if not user:
            user = ctx.message.author
            r = True
        if not r:
            user = user[0]
        embed = discord.Embed(color=0xdd1313)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

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
