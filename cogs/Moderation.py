import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_roles=True)
    async def giverole(self, ctx,  user: discord.Member, role: discord.Role):
        if user and role:
            user.add_roles(roles=role, reason="Give role command")

    @commands.command(pass_context=True)
    async def whois(ctx, *user: discord.Member):
        global data
        data = jsonLoad()
        r = False
        if not user:
            user = ctx.message.author
            r = True
            print("ok")
        if not r:
            user = user[0]
        v = []
        k = user.roles
        print(k)
        if len(k) > 1:
            for over in k:
                if over.name != "@everyone":
                    print(over)
                    t = over.mention
                    print(t)
                    v.append(t)
        text = ""
        if len(k) == 1:
            v.append("No roles")
        for i in v:
            if text != "":
                text = text + ", " + i
            if text == "":
                text = i
        b = user.created_at.strftime("%A, %B %d %Y")
        c = user.joined_at.strftime("%A, %B %d %Y")
        f = user.status
        urk = user.activity
        f = str(f)
        if f == "online":
            f = "**Online**"
        if f == "idle":
            f = "**Idle**"
        if f == "offline":
            f = "**Offline**"
        w = data[str(user.id)]
        print("role: " + text)
        if text == "":
            text = "No Roles"
        print(urk)
        embed = discord.Embed(title=user.name + "#" + user.discriminator, description=user.mention, color=0xe41438)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Nickname", value=user.display_name, inline=True)
        embed.add_field(name="Status", value=f, inline=False)
        embed.add_field(name="Playing", value=urk, inline=True)
        embed.add_field(name="Account Created", value=b, inline=False)
        embed.add_field(name="Joined on", value=c, inline=False)
        embed.add_field(name="Roles", value=str(text), inline=False)
        embed.add_field(name="Warns", value=w["Warns"], inline=False)
        embed.add_field(name="Status", value=w["Status"], inline=False)
        print(embed.fields)
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
    async def addmod(ctx, user: discord.Member, rank):
        w=False
        if mods[str(ctx.message.author.id)] >= 255 and mods[str(ctx.message.author.id)] > int(rank):
            if str(user.id) in mods:
                if mods[str(user.id)] >= mods[str(ctx.message.author.id)]:
                    w=True
            if not w:
                mods[str(user.id)] = int(rank)
                jsonUpdateMods()
                await ctx.send("User " + user.display_name + " is now a rank " + str(rank) + " mod")
            else:
                await ctx.send("Nice try but you can't do that")

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *reason):
        reason = " ".join(reason)
        ctx.guild.ban(user=member, reason=reason)

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *reason):
        reason = " ".join(reason)
        ctx.guild.kick(user=member, reason=reason)

    @commands.command()
    @has_permissions(manage_roles=True)
    async def removerole(self, ctx,  user: discord.Member, role: discord.Role):
        if user and role:
            user.remove_roles(roles=role, reason="Remove role command")

def setup(bot):
    bot.add_cog(Moderation(bot))
