import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def kill(ctx, arg):
        await ctx.send(arg + " is dead")

    @commands.command()
    async def suicide(ctx):
        await ctx.send("https://www.mext.go.jp/a_menu/shotou/seitoshidou/1302907.htm")

    @commands.command(pass_context=True)
    async def cl(ctx, word1, word2):
        word1 = str(word1)
        word2 = str(word2)
        x = []
        for letter in word1:
            for letter2 in word2:
                if str.lower(letter2) == str.lower(letter):
                    if letter in x:
                        pass
                    else:
                        x.append(str.lower(letter))
        v = str(x)
        v = v.replace("'", "")
        v = v.replace("[", "")
        v = v.replace("]", "")
        await ctx.send(v)

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
    async def pfp(ctx, *user: discord.Member):
        r = False
        if not user:
            user = ctx.message.author
            r = True
        if not r:
            user = user[0]
        await ctx.send(user.avatar_url)

    @commands.command(pass_context=True)
    async def love(ctx, *tuple):
        if len(tuple) > 1:
            if tuple[0] == "Xuning" and tuple[1] == "Nancy":
                await ctx.send("100" + "% Compatible")
            else:
                await ctx.send(str(random.randint(0, 100)) + "% Compatible")
        else:
            await ctx.send(str(random.randint(0,100)) + "% Compatible")


def setup(bot):
    bot.add_cog(Fun(bot))
