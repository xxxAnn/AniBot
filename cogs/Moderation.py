import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions
from Libraries.Library import get_guild_language, command_activated, embed_template
from datetime import datetime
import inspect

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        embed = await embed_template("Purge", "Succesfully purged {} messages".format(amount))
        await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(manage_roles=True)
    async def giverole(self, ctx,  user: discord.Member, role: discord.Role):
        if user and role:
            await user.add_roles(role, reason="Give role command")
        embed = discord.Embed(color=0xdd1313)
        embed.add_field(name="Add role", value="Successfully added role")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def whois(self, ctx, *user):
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
        print("role: " + text)
        if text == "":
            text = "No Roles"
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
        embed = discord.Embed(color=0xdd1313)
        embed.add_field(name="Ban", value="Successfully banned user")
        await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *reason):
        reason = " ".join(reason)
        await ctx.guild.kick(user=member, reason=reason)
        embed = discord.Embed()
        embed.add_field(name="Kick", value="Successfully kicked user")
        await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(manage_roles=True)
    async def removerole(self, ctx,  user: discord.Member, role: discord.Role):
        if user and role:
            await user.remove_roles(role, reason="Remove role command")
        embed = discord.Embed(color=0xdd1313)
        embed.add_field(name="Remove role", value="Successfully removed role")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
