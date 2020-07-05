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


async def guild_in_database(guild_id: int):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM levels")
    for x in mycursor:
        # // print(str(x[0]) + "\n" + str(guild_id) + "\n\n")
        if x[0] == guild_id:
            return True
    return False


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


class level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check_guild_data(self, ctx):
        guild_data = await load_guild_data(ctx.guild.id)
        await ctx.send(str(guild_data))


def setup(bot):
    bot.add_cog(level(bot))
