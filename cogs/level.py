import discord, os
from discord.ext import commands
import time
import json
import random
from random import randint
from datetime import datetime
from time import sleep
import operator
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password='123abc',
  database="money"
)


cooldown = {0: 0}


async def guild_in_database(guild_id: int):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM levels")
    for x in mycursor:
        # // print(str(x[0]) + "\n" + str(guild_id) + "\n\n")
        if x[0] == guild_id:
            return True
    return False


async def get_guild_settings(guild_id: str):
    with open('data/settings.json', 'r') as f:
        x = f.read()
        content = json.loads(x)
    if guild_id in content:
        guild_full_data = content[guild_id]
        if 'level_cog' in guild_full_data:
            return guild_full_data['level_cog']
        else:
            content[guild_id]['level_cog'] = {'average_exp': 15, 'exp_roles': {}}
            return content[guild_id]['level_cog']
    else:
        content[guild_id] = {'Language': 'en', 'level_cog': {'average_exp': 15, 'exp_roles': {}}}
        return content[guild_id]['level_cog']
    with open('data/settings.json', 'w') as f:
        x = json.dumps(content)
        f.write(x)


async def load_guild_data(guild_id: int):
    in_database = await guild_in_database(guild_id)
    if in_database:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM levels WHERE id = {0}".format(guild_id))
        myresult = mycursor.fetchone()
        return json.loads(myresult[1])
    else:
        print('hey, that guild is new')
        dict = json.dumps({'0': '0'})
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO levels (id, data) VALUES (%s, %s)", (guild_id, dict))
        return json.loads(dict)


async def save_guild_data(guild_id: int, data):
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE levels SET data = (%s) WHERE id = {0}".format(guild_id), (json.dumps(data),))
    mydb.commit()
    return "Succesful"


class level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild:
            guild_data = await load_guild_data(message.guild.id)
            member = message.author
            if member.id in cooldown:
                member_cooldown = cooldown[member.id]
                if time.time() - member_cooldown > 0:
                    if str(member.id) in guild_data:
                        guild_data[str(member.id)]["exp"]+=randint(15,25)
                    else:
                        guild_data[str(member.id)] = {"exp": 0}
                    await save_guild_data(message.guild.id, guild_data)
            else:
                cooldown[member.id] = time.time()

    @commands.command()
    async def exp(self, ctx):
        if ctx.guild:
            guild_data = await load_guild_data(ctx.guild.id)
            member = ctx.author
            if str(member.id) in guild_data:
                exp = guild_data[str(member.id)]['exp']
            else:
                guild_data[str(member.id)] = {"exp": 0}
                await save_guild_data(ctx.guild.id, guild_data)
                exp = guild_data[str(member.id)]['exp']
            embed=discord.Embed(title=member.display_name, description="Shows the user's experience points.", color=0x0c72df)
            embed.add_field(name="Exp", value="{0}".format(exp), inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['ranks'])
    async def leveltop(self, ctx):
        guild_data = await load_guild_data(ctx.guild.id)
        exp = {}
        for i in guild_data:
            if "exp" in guild_data[i]:
                x = guild_data[i]
                exp[i] = x["exp"]
        sortedExp = sorted(exp.items(), key=operator.itemgetter(1))
        sortedExp = list(reversed(sortedExp))
        string = "```pl\n"
        for x in range(0, 10):
            try:
                txt = str(sortedExp[x][0])
            except:
                break
            loop_user = self.bot.get_user(int(txt))
            val = guild_data[txt]["exp"]
            val = f'{val:,}'.format(val=val)
            string = string + "{" + str(x + 1) + "}     #" + loop_user.name + "\n        Exp : [" + str(val) + "] " + "\n"
        string = string + '```'
        await ctx.send(string)


def setup(bot):
    bot.add_cog(level(bot))
