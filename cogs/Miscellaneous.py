import discord
from discord.ext import commands


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def members(ctx, rolename: discord.Role):
        mm = ctx.message.guild.members
        embed = discord.Embed(title="Members", description="in " + str(rolename), color=0x0d20a4)
        for tm in mm:
            if rolename in tm.roles:
                embed.add_field(name=tm.display_name, value=tm.mention, inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def warn(ctx, user: discord.Member, *cont):
        global data
        data = jsonLoad()
        global mods
        mods = jsonLoadMods()
        print("command attempt")
        if str(ctx.message.author.id) in mods:
            w = False
            if str(user.id) in mods:
                if mods[str(user.id)] >= mods[str(ctx.message.author.id)]:
                    print('this')
                    w = True
            if mods[str(ctx.message.author.id)] > 0 and not w:
                stro = ""
                for i in cont:
                    stro = stro + i + " "
                await user.send("You have been warned for the following reason: \n" + stro)
                w = data[str(user.id)]
                w["Warns"] = str(int(w["Warns"]) + 1)
                x = str(user.id) + " has been warned for "+ stro + " on " + str(datetime.date(datetime.now())) + "\n"
                with open("WarnLog.txt", "a") as f:
                    f.write(x)
                    f.close()
                w = data[str(user.id)]
                jsonUpdate()
                await ctx.message.delete()
            else:
                await ctx.send("You do not have permission to do this")
        else:
            await ctx.send("You do not have permission to do this")

    @commands.command(pass_context=True)
    async def react(ctx, arg):
        msg = ctx.message
        await msg.add_reaction(arg)
        x = await ctx.send(arg)
        time.sleep(0.2)
        await x.delete()
        print(arg)

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
