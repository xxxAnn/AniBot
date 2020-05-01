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


def setup(bot):
    bot.add_cog(Moderation(bot))