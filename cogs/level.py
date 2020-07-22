import discord, os
from discord.ext import commands
from discord.ext.commands import has_permissions
from Libraries.Library import get_guild_language, Pages, command_activated
import time
import json
import random
from random import randint
from datetime import datetime
from time import sleep
import operator
import mysql.connector
import inspect


cooldown = {0: 0}

# // returns a sql
async def get_sql(host_value='localhost', user_value='root', password_value='123abc', database_value='money'):
    config = {
    'host': host_value,
    'user': user_value,
    'password': password_value,
    'database': database_value,
    }
    return mysql.connector.connect(**config)

# // Checks if the guild is in database \\ #
async def guild_in_database(guild_id: int):
    mydb = await get_sql()
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT * FROM levels")
    for x in mycursor:
        # print(str(x[0]) + "\n" + str(guild_id) + "\n\n")
        if x[0] == guild_id:
            return True
    return False

# // Returns the guild settings from the settings.json file \\ #
async def get_guild_settings(guild_id: str):
    return_content = None
    guild_id = str(guild_id)
    with open('data/settings.json', 'r') as f:
        x = f.read()
        content = json.loads(x)
    if guild_id in content:
        guild_full_data = content[guild_id]
        if 'level_cog' in guild_full_data:
            return_content = guild_full_data['level_cog']
        else:
            content[guild_id]['level_cog'] = {'average_exp': 15, 'exp_roles': {}}
            return_content = content[guild_id]['level_cog']
    else:
        content[guild_id] = {'Language': 'en', 'level_cog': {'average_exp': 15, 'exp_roles': {}}}
        return_content = content[guild_id]['level_cog']
    with open('data/settings.json', 'w') as f:
        x = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
        f.write(x)
    return return_content

# // Loads the guild's data from the MySQL database \\ #
async def load_guild_data(guild_id: int):
    mydb = await get_sql()
    in_database = await guild_in_database(guild_id)
    if in_database:
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM levels WHERE id = {0}".format(guild_id))
        myresult = mycursor.fetchone()
        return json.loads(myresult[1])
    else:
        dict = json.dumps({'0': '0'})
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("INSERT INTO levels (id, data) VALUES (%s, %s)", (guild_id, dict))
        mydb.commit()
        return json.loads(dict)

# // Saves the data into the MySQL database \\ #
async def save_guild_data(guild_id: int, data):
    mydb = await get_sql()
    mycursor = mydb.cursor(buffered=True)
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
                    # // Remember that the key in exp_roles is a string \\ #
                    if str(member.id) in guild_data:
                        before_exp = guild_data[str(member.id)]["exp"]
                        guild_settings = await get_guild_settings(message.guild.id)
                        avrg_exp = int(guild_settings['average_exp'])
                        guild_data[str(member.id)]["exp"]+=randint(avrg_exp-int(avrg_exp/10), avrg_exp+int(avrg_exp/10))
                        after_exp = guild_data[str(member.id)]["exp"]
                        for exp_required in guild_settings['exp_roles'].keys():
                            exp_required = int(exp_required)
                            if before_exp<exp_required and after_exp>exp_required:
                                role = message.guild.get_role(int(guild_settings['exp_roles'][str(exp_required)]))
                                await member.add_roles(role)
                                await message.channel.send("You've been awarded the {0} role".format(role.name))
                    else:
                        guild_data[str(member.id)] = {"exp": 0}
                    await save_guild_data(message.guild.id, guild_data)
            else:
                cooldown[member.id] = time.time()

    @commands.command()
    async def exp(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
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
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
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
            if loop_user:
                pass
            else:
                break
            val = guild_data[txt]["exp"]
            val = f'{val:,}'.format(val=val)
            string = string + "{" + str(x + 1) + "}     #" + loop_user.name + "\n        Exp : [" + str(val) + "] " + "\n"
        string = string + '```'
        await ctx.send(string)

    @commands.command()
    @has_permissions(administrator=True)
    async def set_exp_gain(self, ctx, value: int):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        guild_settings = await get_guild_settings(ctx.guild.id)
        with open('data/settings.json', 'r') as f:
            x = f.read()
            content = json.loads(x)
        content[str(ctx.guild.id)]['level_cog']['average_exp'] = value
        with open('data/settings.json', 'w') as f:
            x = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
            f.write(x)
            await ctx.send("Successfully changed exp gain")


    @commands.command()
    @has_permissions(administrator=True)
    async def create_exp_role(self, ctx, exp: int, role: discord.Role):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        exp = str(exp)
        guild_settings = await get_guild_settings(ctx.guild.id)
        with open('data/settings.json', 'r') as f:
            x = f.read()
            content = json.loads(x)
        content[str(ctx.guild.id)]['level_cog']['exp_roles'][exp] = int(role.id)
        with open('data/settings.json', 'w') as f:
            x = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
            f.write(x)
            await ctx.send("Successfully added level role")

    @commands.command()
    @has_permissions(administrator=True)
    async def delete_exp_role(self, ctx, exp: int):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        exp = str(exp)
        guild_settings = await get_guild_settings(ctx.guild.id)
        with open('data/settings.json', 'r') as f:
            x = f.read()
            content = json.loads(x)
        if exp in content[str(ctx.guild.id)]['level_cog']['exp_roles']:
            content[str(ctx.guild.id)]['level_cog']['exp_roles'].pop(exp)
        else:
            await ctx.send("No such binding was found")
        with open('data/settings.json', 'w') as f:
            x = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
            f.write(x)
            await ctx.send("Successfully removed level role")



def setup(bot):
    bot.add_cog(level(bot))
