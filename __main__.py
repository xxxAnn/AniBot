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
initial_extensions = ['cogs.Fun', 'cogs.Moderation']
BOT_PREFIX = "%"
TOKEN = token_const
client = Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
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


@client.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    usersList = [331431342438875137]
    bannedRoles = [695789139953451110, 655489817823674369, 678752359425507378]
    if ctx.author.id in usersList:
        if role.id not in bannedRoles:
            await member.remove_roles(role)
            await ctx.send("successfully removed role")
        else:
            await ctx.send("you can't remove that role")
    else:
        await ctx.send("you can't use that command")


@client.command()
async def online(ctx):
    mem = ctx.message.guild.members
    embed = discord.Embed(title="Online", description="Online Members", color=0x0d20a4)
    for i in mem:
        k = str(i.status)
        if k == "online" or k == "idle" or k == "dnd":
            if not i.bot:
                embed.add_field(name="*" + i.display_name + "*", value=i.mention, inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def ismod(ctx, user: discord.Member):
    global mods
    mods = jsonLoadMods()
    if str(user.id) in mods:
        await ctx.send("Rank: " + str(mods[str(user.id)]) + " Mod")
    else:
        await ctx.send("Nope")
@client.command()
async def kill(ctx, arg):
    await ctx.send(arg + " is dead")


@client.command()
async def suicide(ctx):
    await ctx.send(ctx.message.author.mention + " is now dead")


@client.command()
async def presentations(ctx):
    await ctx.send("I am 高木さん the superior anime character from the best anime ever, you disagree ?, fight me !")


@client.command()
async def define(ctx, arg):
    if 0 == 1:
        arg = str(arg)
        v = dictionary.meaning(arg)
        k = ""
        d = 0
        if str(v) == "None":
            await ctx.send("No definition found")
        if str(v) != "None":
            if "Noun" in v:
                c = v["Noun"]
                r = 0
                for i in c:
                    d = d + 1
                    k = str(k + "\n" + "*" + str(d) + ": " + c[r] + "*")
                    r = r + 1
                    if d > 1:
                        break
                    print(k)
            if "Verb" in v:
                c = v["Verb"]
                r = 0
                for i in c:
                    d = d + 1
                    k = str(k + "\n" + "*" + str(d) + ": " + c[r] + "*")
                    r = r + 1
                    if d > 1:
                        break
                    print(k)
            if "Pronoun" in v:
                c = v["Pronoun"]
                r = 0
                for i in c:
                    d = d + 1
                    k = str(k + "\n" + "*" + str(d) + ": " + c[r] + "*")
                    r = r + 1
                    if d > 1:
                        break
                    print(k)
            if "Adverb" in v:
                c = v["Adverb"]
                r = 0
                for i in c:
                    d = d + 1
                    k = str(k + "\n" + "*" + str(d) + ": " + c[r] + "*")
                    r = r + 1
                    if d > 1:
                        break
                    print(k)
            if "Article" in v:
                c = v["Article"]
                r = 0
                for i in c:
                    d = d + 1
                    k = str(k + "\n" + "*" + str(d) + ": " + c[r] + "*")
                    r = r + 1
                    if d > 1:
                        break
                    print(k)
            if "Adjective" in v:
                c = v["Adjective"]
                r = 0
                for i in c:
                    d = d + 1
                    k = str(k + "\n" + "*" + str(d) + ": " + c[r] + "*")
                    r = r + 1
                    if d > 1:
                        break
                    print(str(c))
            await ctx.send('\nMeaning(s) : ' + k)
    else:
        await ctx.send("This command is currently disabled")


@client.command()
async def say(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(arg)


@client.command()
async def cookie(ctx, arg):
    await ctx.send(arg + " gets a cookie")


@client.command(pass_context=True)
async def invite(ctx):
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=618166814685265931&scope=bot&permissions=8")


@client.command(pass_context=True)
async def question(ctx, *, arg):
    y = ["yes", "no", "probably", "definitely not", "are you dumb ?", "No u", "Definitely",
         "I LOVE IT WHEN U CALL ME SEÑORITA"]
    x = random.choice(y)
    await ctx.send(x)


@client.command(pass_context=True)
async def react(ctx, arg):
    msg = ctx.message
    await msg.add_reaction(arg)
    x = await ctx.send(arg)
    time.sleep(0.2)
    await x.delete()
    print(arg)


@client.command(pass_context=True)
async def oldest(ctx):
    peeps = ctx.message.guild.members
    largestyear = 2019
    largestmonth = 12
    largestday = 31
    usera = "t"
    kd = []
    amount = 0
    for i in peeps:
        if i.bot is False and i.id != 272388174838497280:
            month = int(i.created_at.strftime("%m"))
            day = int(i.created_at.strftime("%d"))
            year = int(i.created_at.strftime("%Y"))
            month = str(month)
            year = str(year)
            day = str(day)
            largestmonth = str(largestmonth)
            largestyear = str(largestyear)
            largestday = str(largestday)
            #print(i.name + " " + day + "/"+ month +"/"+ year + " " + largestday + "/" + largestmonth + "/" + largestyear )
            month = int(month)
            year = int(year)
            day = int(day)
            largestmonth = int(largestmonth)
            largestyear = int(largestyear)
            largestday = int(largestday)
            if year < largestyear:
                kd.append(i)
                largestday = day
                largestyear = year
                largestmonth = month
            if year == largestyear:
                if month < largestmonth:
                    kd.append(i)
                    largestday = day
                    largestyear = year
                    largestmonth = month
                    t = largestday + 1
                if month == largestmonth:
                    if day < largestday + 1:
                        largestday = day
                        kd.append(i)
    kd = list(dict.fromkeys(kd))
    for x in kd:
        #print(x.name + str(x.id))
        month = int(x.created_at.strftime("%m"))
        day = int(x.created_at.strftime("%d"))
        year = int(x.created_at.strftime("%Y"))
        if month < largestmonth + 1 and day < largestday + 1 and year < largestyear + 1 and x.id != 272388174838497280:
            if usera == "t":
                usera = x.name + ", " + x.display_name
            else:
                usera = usera + "\n" + x.name + ", " + x.display_name
    await ctx.send("```" + usera + "\n" + "```")


@client.command(pass_context=True)
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


@client.command(pass_context=True)
async def spam(ctx):
    await ctx.send("This command is currently disabled")


@client.command(pass_context=True)
async def pfp(ctx, *user: discord.Member):
    r = False
    if not user:
        user = ctx.message.author
        r = True
    if not r:
        user = user[0]
    await ctx.send(user.avatar_url)


@client.command(pass_context=True)
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


@client.command(pass_context=True)
async def members(ctx, rolename: discord.Role):
    mm = ctx.message.guild.members
    embed = discord.Embed(title="Members", description="in " + str(rolename), color=0x0d20a4)
    for tm in mm:
        if rolename in tm.roles:
            embed.add_field(name=tm.display_name, value=tm.mention, inline=True)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def exp(ctx):
    await ctx.send("12")


@client.command(pass_context=True)
async def love(ctx, *tuple):
    if len(tuple) > 1:
        if tuple[0] == "Xuning" and tuple[1] == "Nancy":
            await ctx.send("100" + "% Compatible")
        else:
            await ctx.send(str(random.randint(0, 100)) + "% Compatible")
    else:
        await ctx.send(str(random.randint(0,100)) + "% Compatible")
@client.command(pass_context=True)
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
@client.command(pass_context=True)
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


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send(":negative_squared_cross_mark: Bad Argument.")
        return
    if isinstance(error, CommandNotFound):
        await ctx.send("Hey chill I can't do that. \n *nor do I want to tbh*")
        return
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Missing arguments")
        return
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("There was an error executing that command")
        raise error
        return
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Missing permissions")
    raise error


client.run(TOKEN)
