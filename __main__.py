import os, discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import CommandNotFound
from discord.voice_client import VoiceClient
import time
import random
from PyDictionary import PyDictionary
import json
import discord
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from datetime import datetime
from data.secret import token_const


def get_prefix(bot, msg):
    '''
    default_prefix = '-'

    '''
    prefixes = []
    if msg.guild is None:
        prefixes.append('-')
    else:
        guild_id = str(msg.guild.id)
        with open("data/settings.json", "r") as f:
            x = f.read()
            content = json.loads(x)
            f.close()
        if guild_id in content:
            if 'prefix' in content[guild_id]:
                prefixes.append(content[guild_id]['prefix'])
            else:
                prefixes.append('-')
        else:
            prefixes.append('-')
    return prefixes
    

initial_extensions = ['cogs.Fun', 'cogs.Moderation', 'cogs.Miscellaneous', 'cogs.Money', 'cogs.level']


TOKEN = token_const
client = Bot(command_prefix=get_prefix, case_insensitive=True)
client.case_insensitive = True


if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with your feelings", type=1))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.BadArgument):
        embed = discord.Embed(color=0xdd1313)
        embed.set_image(url="https://thumbs.gfycat.com/DismalWarmArmadillo-max-1mb.gif")
        await ctx.send(embed=embed)
        await ctx.send(":negative_squared_cross_mark: Bad Argument.")
        return
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(color=0xdd1313)
        embed.set_image(url="https://thumbs.gfycat.com/DismalWarmArmadillo-max-1mb.gif")
        await ctx.send(embed=embed)
        await ctx.send("Missing arguments")
        return
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        embed = discord.Embed(color=0xdd1313)
        embed.set_image(url="https://media1.tenor.com/images/f1187d7f7d745182879263e0b125e2eb/tenor.gif?itemid=7906629")
        await ctx.send(embed=embed)
        await ctx.send("Something unexpected happened")
        raise error
        return
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Missing permissions")
    raise error


client.run(TOKEN)
