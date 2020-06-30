import discord, os
from discord.ext import commands
import time
import json
import random
from random import randint
from datetime import datetime
from time import sleep
import operator
class Inventory:
    def __init__(self, content, content_literal):
        self.content = content
        self.legacy_deprecated_content_literal = content_literal

    def has(self, selectid: str):
        for item in self.content:
            if str(item.id) == selectid:
                return item
        return False

    def get(self, selectid: str):
        for item in self.content:
            if str(item.id) == selectid:
                return item
        return None

    def add(self, item):
        self.content.append(item)

class Shop:
    def __init__(self, owner, inv, name):
        self.owner = owner
        self.inv = inv
        self.name = name
        self.id = str(id)

    def save(self):
        global data
        data = jsonLoad()
        content_literal = toContentLiteral(self.inv.content)
        data["Shops"][self.id]["Inventory"] = content_literal


class Item:
    def __init__(self, id, name, amount, exclusive):
        self.id = str(id)
        self.name = name
        self.amount = amount
        self.exclusive = exclusive


class Player:

    def __init__(self, inventory, money, energy, id):
        self.inventory = inventory
        self.money = money
        self.energy = energy
        self.id = str(id)

    def save(self):
        global data
        data = jsonLoad()
        if self.id not in data:
            data[self.id] = {"Energy": None, "Money": None, "Inventory": None}
        data[self.id]["Energy"] = self.energy
        data[self.id]["Money"] = self.money
        content_literal = toContentLiteral(self.inventory.content)
        data[self.id]["Inventory"] = content_literal
        jsonUpdate(data)


def jsonUpdate(data):
    d = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    with open("Money.json", "w") as file:
        file.write(d)


def toContentLiteral(inventoryContentItem):
    literal_list = []
    for item in inventoryContentItem:
        x = {"Id": item.id, "Name": item.name, "Amount": item.amount, "Exclusive": item.exclusive}
        literal_list.append(x)
    return literal_list


def cram():
    with open("Cram.json", "r") as f:
        x = f.read()
        return json.loads(x)

def constructPlayer(id):
    id = str(id)
    global data
    data = jsonLoad()
    if id not in data:
        data[id] = {"Money": 0, "Inventory": [], "Energy": {"Val": 10, "Recover": int(time.time())}}
    listContent = []
    for i in data[id]["Inventory"]:
        x = Item(i["Id"], i["Name"], i["Amount"], i["Exclusive"])
        listContent.append(x)
    inventoryObject = Inventory(listContent, data[id]["Inventory"])
    playerObject = Player(inventoryObject, data[id]["Money"], data[id]["Energy"], id=id)
    return playerObject

def constructShop(shopId):
    global data
    data = jsonLoad()
    listContent = []
    for i in data["Shops"][shopId]["Inventory"]:
        x = Item(i["Id"], i["Name"], i["Amount"], i["Exclusive"])
        listContent.append(x)
    inventoryObject = Inventory(listContent, data[id]["Inventory"])
    shopObject = Shop(data["Shops"][shopId]["Owner"], inventoryObject, data["Shops"][shopId], shopId)
    return shopObject


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx, *user: discord.Member):
        if not user:
            user = ctx.message.author
        else:
            user = user[0]
        id = str(user.id)
        player = constructPlayer(user.id)
        embed = discord.Embed(title="{0}'s balance".format(user.display_name))
        embed.add_field(name="Money:", value="{0}{1}".format(player.money, data["Currency"]), inline=True)
        await ctx.send(embed=embed)
        player.save()


def setup(bot):
    bot.add_cog(Economy(bot))
