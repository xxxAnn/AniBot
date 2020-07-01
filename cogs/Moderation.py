import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions
from datetime import datetime


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def jsonUpdate(self, data):
        d = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        with open("data/Data.json", "w") as file:
            file.write(d)


    def jsonLoad(self):
        with open("data/Data.json", "r") as f:
            x = f.read()
            return json.loads(x)


    def jsonLoadMods(self):
        with open("data/Mods.Json", "r") as f:
            x = f.read()
            return json.loads(x)


    def jsonUpdateMods(self, mods):
        d = json.dumps(mods)
        with open("data/Mods.Json", "w") as file:
            file.write(d)

    @commands.command()
    @has_permissions(manage_roles=True)
    async def giverole(self, ctx,  user: discord.Member, role: discord.Role):
        if user and role:
            user.add_roles(roles=role, reason="Give role command")

    @commands.command(pass_context=True)
    async def whois(self, ctx, *user: discord.Member):
        global data
        data = self.jsonLoad()
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
        print(embed.fields)
        await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *reason):
        reason = " ".join(reason)
        ctx.guild.ban(user=member, reason=reason)

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *reason):
        reason = " ".join(reason)
        await ctx.guild.kick(user=member, reason=reason)

    @commands.command()
    @has_permissions(manage_roles=True)
    async def removerole(self, ctx,  user: discord.Member, role: discord.Role):
        if user and role:
            user.remove_roles(roles=role, reason="Remove role command")

def setup(bot):
    bot.add_cog(Moderation(bot))
