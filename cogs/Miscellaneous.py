import discord
from discord.ext import commands


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def online(self, ctx):
        mem = ctx.message.guild.members
        embed = discord.Embed(title="Online", description="Shows a list of online members", color=0x0d20a4)
        temp = ""
        for i in mem:
            k = str(i.status)
            if k == "online" or k == "idle" or k == "dnd":
                if not i.bot:
                    temp+=i.mention+"\n"
        embed.add_field(name="Online members:", value=temp, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discordapp.com/oauth2/authorize?client_id=618166814685265931&scope=bot&permissions=8")

    @commands.command(aliases=['8ball'])
    async def question(self, ctx, *, arg):
        y = ["yes", "no", "probably", "definitely not", "ofc not?", "you'll soon know", "definitely", ]
        x = random.choice(y)
        await ctx.send(x)

    @commands.command(pass_context=True)
    async def oldest(self, ctx):
        list_ids = []
        smallest = 999999999999999999999
        for i in ctx.guild.members:
            if i.id < smallest:
                smallest = i.id
        await ctx.send(ctx.guild.get_member(smallest).display_name + " is the oldest member of the guild")


def setup(bot):
    bot.add_cog(Miscellaneous(bot))