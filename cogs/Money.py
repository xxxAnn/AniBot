import discord, os
from discord.ext import commands
import json
import random
from random import randint
from datetime import datetime
import operator
import asyncio
import mysql.connector
from Libraries.Library import Pages, sqlClient, command_activated, embed_template
from Libraries.Economy.items import ItemHandler
from Libraries.Economy.player import PlayerHandler
from Libraries.Economy.shops import ShopHandler
from Libraries.Economy.world import TheWorld
from Libraries.Economy.globals import Waterfall, EconomyHandler
import inspect
import time

# // Loads data from the database \\ #
def jsonLoad():
    client = sqlClient()
    result = client.select("data", "id", "1")
    client.end()
    return json.loads(result[1])

# // Saves data into the database \\ #
def jsonUpdate(data):
    client = sqlClient()
    client.update("data", "jsonColumn", "id", "1", json.dumps(data))
    client.end()

lasttime = int(time.time())

def executeSomething():
    global data
    data = jsonLoad()
    for i in data.keys():
        if "Energy" in data[i]:
            player = PlayerHandler.constructPlayer(i)
            id = int(i)
            if int(time.time()) - data[i]["Energy"]["Recover"] > 299:
                data[i]["Energy"]["Val"] = 10
                player.energy["Val"] = 10
                data[i]["Energy"]["Recover"] = int(time.time())
                player.energy["Recover"] = int(time.time())
                player.save()
            if int(-1*(time.time()-(player.energy["Recover"]+300))) < 0:
                player.energy['Recover'] = time.time()
                player.save()


def cram():
    with open("data/Cram.json", "r") as f:
        x = f.read()
        return json.loads(x)


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fish_activated = {}
        self.fishermen = {}
        self.meta = ItemHandler.metareader()
        self.world_map = TheWorld()

    @commands.command()
    async def idtoname(self, ctx, id: str):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        embed = await embed_template("Pezentry", ItemHandler.get_item(id).name)
        await ctx.send(embed=embed)

    @commands.command()
    async def bal(self, ctx, *user: discord.Member):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        if not user:
            user = ctx.message.author
        else:
            user = user[0]
        if user.bot:
            embed = await embed_template("Pezentry", "Imagine being so lonely you play with a fucking bot")
            await ctx.send(embed=embed)
            return
        id = str(user.id)
        data = jsonLoad()
        player = PlayerHandler.constructPlayer(user.id)
        embed = discord.Embed(title="{0}'s balance".format(user.display_name))
        embed.add_field(name="Money:", value="{0}{1}".format(player.money, data["Currency"]), inline=True)
        await ctx.send(embed=embed)
        player.save()

    @commands.command()
    async def pay(self, ctx, user: discord.Member, amount):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        amount = amount.replace(",", "")
        amount = int(amount)
        if not amount < 0:
            id = str(user.id)
            idc = str(ctx.message.author.id)
            player = PlayerHandler.constructPlayer(id)
            playerc = PlayerHandler.constructPlayer(idc)
            if amount > playerc.money:
                await ctx.send("You ain't got the money")
            else:
                playerc.money -= amount
                player.money += amount
                embed = await embed_template("Pezentry", "Successfully paid user")
                await ctx.send(embed=embed)
            player.save()
            playerc.save()
        else:
            embed = await embed_template("Pezentry", "Stealing is wrong")
            await ctx.send(embed=embed)

    @commands.command()
    async def top(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        global data
        data = jsonLoad()
        exp = {}
        for i in data:
            if "Money" in data[i]:
                x = data[i]
                exp[i] = x["Money"]
        sortedExp = sorted(exp.items(), key=operator.itemgetter(1))
        sortedExp = list(reversed(sortedExp))
        string = "```pl\n"
        for x in range(0, 9):
            try:
                txt = str(sortedExp[x][0])
            except:
                break
            usa = self.bot.get_user(int(txt))
            if not usa:
                continue
            elif usa.bot:
                continue
            val = data[txt]["Money"]
            val = f'{val:,}'.format(val=val)
            string = string + "{" + str(x + 1) + "}     #" + usa.display_name + "\n        Money : [" + str(val) + "] " + data[
                "Currency"] + "\n"
        string = string + '```'
        embed = await embed_template("Pezentry", string)
        await ctx.send(embed=embed)

    @commands.command()
    async def addexcl(self, ctx, *name):
        if ctx.message.author.id == 331431342438875137:
            player = PlayerHandler.constructPlayer(ctx.author.id)
            name = " ".join(name)
            player.inventory + ItemHandler.get_item(amount=1, exclusive=True, name=name, id="273")
            player.save()
        else:
            embed = await embed_template("Pezentry", "Sorry you cant do that lol")
            await ctx.send(embed=embed)


    @commands.command()
    async def craft(self, ctx, item_name, amountx=1):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        user = ctx.message.author
        player = PlayerHandler.constructPlayer(user.id)
        rors = player.craft(item_name, amountx)
        if rors != 20:
            if rors == 1:
                await ctx.message.reply("That item can't be crafted", mention_author=True)
            elif rors == 2:
                await ctx.message.reply("You do not have the required items", mention_author=True)
            elif rors == 3:
                await ctx.message.reply("You do not have enough of the required items", mention_author=True)
            else:
                await ctx.message.reply("An unexpected error has occured", mention_author=True)
        else:
            await ctx.message.reply("Successfully crafted item", mention_author=True)

    @commands.command()
    async def craftable(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        global data
        data= jsonLoad()
        cramed = ItemHandler.metareader()
        string = ""
        for i in cramed.crafts.keys():
            item = cramed.crafts[i]
            text= "**{0}**, Requires Item: **{2}** __x{1}__".format(ItemHandler.get_item(i).name, item["requireditemsamount"][0], ItemHandler.get_item(item['requireditems'][0]).name)
            if len(item['list1'])>1:
                text+= " and Item: **{1}** __x{0}__".format(item["requireditemsamount"][1], ItemHandler.get_item(item['requireditems'][1]).name)
            text+="\n"
            string+=text
        embed = await embed_template("Pezentry", string)
        await ctx.send(embed=embed)

    @commands.command()
    async def energy(self, ctx):
        user = ctx.message.author
        player = PlayerHandler.constructPlayer(user.id)
        executeSomething()
        embed = await embed_template("Pezentry", "{0}/10, Recovers in {1} seconds".format(player.energy["Val"], int(-1*(time.time()-(player.energy["Recover"]+300)))))
        await ctx.send(embed=embed)
        player.save()

    @commands.command()
    async def eat(self, ctx, itemName: str):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        player = PlayerHandler.constructPlayer(ctx.author.id)
        cramed = cram()
        itemId = ItemHandler.id_from_name(itemName)
        if str(itemId) in cramed["Eatables"]:
            if player.inventory.has(itemId) is not False:
                if player.inventory.get(itemId).amount>0:
                    itemX = player.inventory.get(itemId)
                    itemX.amount-=1
                    player.energy["Val"] += cramed["Eatables"][itemId]
                    if player.energy["Val"] > 10:
                        player.energy["Val"] = 10
                    embed = await embed_template("Pezentry", "Replenished {0} energy".format(cramed["Eatables"][itemId]))
                    await ctx.send(embed=embed)
                    player.save()
                else:
                    embed = await embed_template("Pezentry", "Y'aint have that")
                    await ctx.send(embed=embed)
            else:
                embed = await embed_template("Pezentry", "Y'aint have that")
                await ctx.send(embed=embed)
        else:
            embed = await embed_template("Pezentry", "Ya can't that")
            await ctx.send(embed=embed)

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, *user: discord.Member):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        if not user:
            user = ctx.message.author
        else:
            user = user[0]
        player = PlayerHandler.constructPlayer(user.id)
        temp = []
        embed = discord.Embed(title="{0}'s inventory".format(user.display_name))
        for item in player.inventory.content:
            if item.exclusive:
                embed.add_field(name=item.name, value="Exclusive")
                temp.append((item.name) + ": Exclusive")
            else:
                embed.add_field(name=item.name, value=item.amount)
                temp.append(str(item.name) + ": **x{0}**".format(item.amount))
        player.save()
        page = Pages(ctx, entries=temp, custom_title="{0}'s inventory:\n".format(user.display_name))
        await page.paginate()

    @commands.command()
    async def exploit(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        player = PlayerHandler.constructPlayer(ctx.author.id)
        if player.energy["Val"]>0:
            player.energy["Val"]-=1
            result = self.meta.rolls.exploit(self.world_map.get_tile(player.position))
            money = randint(100,500)
            if result != 0:
                if player.inventory.has(result) is not False:
                    invitem = player.inventory.get(result)
                    invitem.amount += (amount := randint(1,3))
                else:
                    invitem = ItemHandler.get_item(result)
                    invitem.amount = (amount := randint(1,3))
                    player.inventory + invitem
            if result == 0:
                embed = await embed_template("Pezentry", "You gained {1}{0}".format(str(money), "$"))
                await ctx.send(embed=embed)
            else:
                embed = await embed_template("Pezentry", "You gained {1}{0} and found {3} x{2}".format(str(money), "$", amount, invitem.name))
                await ctx.send(embed=embed)
        else:
            embed = await embed_template("Pezentry", "No energy sowwy")
            await ctx.send(embed=embed)
        player.save()


    @commands.command()
    async def create_shop(self, ctx, *Name):
        Name = " ".join(Name)
        player = PlayerHandler.constructPlayer(str(ctx.author.id))
        if player.money >= 5000:
            player.money-=5000
            response, id = ShopHandler.createShop(name=Name, ownerId=str(ctx.author.id))
            if isinstance(response, EconomyHandler.Success):
                embed = await embed_template("Pezentry", str(response)+"\n Paid 5,000 and bought a level one shop")
                await ctx.send(embed=embed)
                player.save()
            else:
                embed = await embed_template("Pezentry", str(response))
                await ctx.send(embed=embed)
        else:
            embed = await embed_template("Pezentry", "You don't have the money")
            await ctx.send(embed=embed)

    @commands.command()
    async def view_shop(self, ctx, *Name):
        Name = " ".join(Name)
        shop = ShopHandler.findShopFromName(Name)
        if not isinstance(shop, str):
            embed = discord.Embed(title="{}".format(shop), description="Shows the shop's inventory", color=0xdd1313)
            if len(shop.inv.content) == 0:
                embed.add_field(name="There are no items in this shop", value="Come back later")
            else:
                for item in shop.inv.content:
                    embed.add_field(name="{0} x{1}".format(item.name, item.amount), value="Buy for {0}$".format(item.price))
            await ctx.send(embed=embed)
        else:
            raise discord.ext.commands.errors.BadArgument

    @commands.command()
    async def sell(self, ctx, item, price: int, amount: int, *shopName):
        shopName = " ".join(shopName)
        if ItemHandler.id_from_name(item) == "Not Found" or ShopHandler.findShopFromName(shopName) == "Not Found" or isinstance(price, int) == False or isinstance(amount, int) == False: raise discord.ext.commands.errors.BadArgument
        shop = ShopHandler.findShopFromName(shopName)
        if str(shop.owner) == str(ctx.author.id):
            itemId = ItemHandler.id_from_name(item)
            item = ItemHandler.get_item(str(itemId))
            player = PlayerHandler.constructPlayer(str(ctx.author.id))
            if player.inventory.has(str(item.id)):
                player_inv_item = player.inventory.has(str(item.id))
                if player_inv_item.amount >= amount:
                    response = shop.add_item(ItemHandler.Item(id=player_inv_item.id, name=player_inv_item.name, amount=player_inv_item.amount, exclusive=player_inv_item.exclusive), int(amount), int(price))
                    if isinstance(response, EconomyHandler.Success):
                        player_inv_item.amount-=int(amount)
                        shop.save()
                        player.save()
                        embed = await embed_template("Pezentry", "Successfully put item to sold")
                        await ctx.send(embed=embed)
                    else:
                        embed = await embed_template("Pezentry", str(response))
                        await ctx.send(embed=embed)
                else:
                    embed = await embed_template("Pezentry", "You don't have enough of that item")
                    await ctx.send(embed=embed)
            else:
                embed = await embed_template("Pezentry", "You don't have that item")
                await ctx.send(embed=embed)
        else:
            embed = await embed_template("Pezentry", "This isn't your shop")
            await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item, amount:int, *shopName):
        shopName = " ".join(shopName)
        if ItemHandler.id_from_name(item) == "Not Found" or ShopHandler.findShopFromName(shopName) == "Not Found" or isinstance(amount, int) == False: raise discord.ext.commands.errors.BadArgument
        shop = ShopHandler.findShopFromName(shopName)
        itemId = ItemHandler.id_from_name(item)
        player = PlayerHandler.constructPlayer(ctx.author.id)
        if shop.inv.has(itemId):
            shopItem = shop.inv.get(itemId)
            if player.money >= shopItem.price*amount:
                # / Transferring the money
                player.money-=shopItem.price*amount
                shopOwner = PlayerHandler.constructPlayer(shop.owner)
                shopOwner.money+=shopItem.price*amount
                # / Transfering the item
                shopItem.amount-=amount
                newItem = ItemHandler.get_item(id=shopItem.id,amount=amount)
                player.inventory + newItem
                # / Saving
                shopOwner.save()
                player.save()
                shop.save()
                embed = await embed_template("Pezentry", "Successfully bought item")
                await ctx.send(embed=embed)
            else:
                embed = await embed_template("Pezentry", "You don't have the money")
                await ctx.send(embed=embed)
        else:
            embed = await embed_template("Pezentry", "This item is not for sold")
            await ctx.send(embed=embed)

    @commands.command()
    async def set_money(self, ctx, user: discord.Member=None, amount:int=50000):
        if ctx.author.id == 331431342438875137:
            uza = PlayerHandler.constructPlayer(user.id)
            uza.money=amount
            uza.save()
        else:
            embed = await embed_template("Pezentry", "You can't do that silly")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fish(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        self.fish_activated[ctx.author.id] = 0
        embed = discord.Embed(title="Fishing", description="Click the reaction at the right time to catch a fish")
        embed.add_field(name="Indicator", value="🔵")
        fish_message = await ctx.send(embed=embed)
        self.fishermen[fish_message.id] = ctx.author.id
        await fish_message.add_reaction("🎣")
        delay = randint(5, 10)
        await asyncio.sleep(delay)
        self.fish_activated[ctx.author.id] = 1
        new_embed = discord.Embed(title="Fishing", description="Click the reaction at the right time to catch a fish")
        new_embed.add_field(name="Indicator", value="🐟")
        await fish_message.edit(embed=new_embed)
        await asyncio.sleep(2)
        self.fish_activated[ctx.author.id] = 2
        await asyncio.sleep(5)
        await fish_message.clear_reactions()

    async def check_for_fishing(self, playload):
        id = playload.user_id
        if self.fish_activated[id] == 0:
            message = await self.get_message_from_playload(playload)
            await message.clear_reactions()
            channel = self.bot.get_channel(playload.channel_id)
            embed = await embed_template("Pezentry", "Too quick")
            await channel.send(embed=embed)
        elif self.fish_activated[id] == 1:
            message = await self.get_message_from_playload(playload)
            await message.delete()
            # / Give the fish
            items = self.meta.fishable
            weights = self.meta.fishweights
            result = random.choices(items, weights)[0]
            player = PlayerHandler.constructPlayer(playload.user_id)
            if result != 0:
                item = ItemHandler.get_item(id=result)
                item.amount = (amount := randint(1,3))
                player.inventory + item
                player.save()
                embed = await embed_template("Pezentry", "You got {0} x{1}".format(item.name, amount))
            else:
                embed = await embed_template("Pezentry", "You got nothing")
            await message.channel.send(embed=embed)
        elif self.fish_activated[id] == 2:
            message = await self.get_message_from_playload(playload)
            channel = self.bot.get_channel(playload.channel_id)
            await message.clear_reactions()
            embed = await embed_template("Pezentry", "Too slow")
            await channel.send(embed=embed)

    async def get_message_from_playload(self, playload):
        channel = self.bot.get_channel(playload.channel_id)
        return await channel.fetch_message(playload.message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, playload):
        emoji = str(playload.emoji)
        if emoji == "🎣":
            if playload.message_id in self.fishermen:
                if self.fishermen[playload.message_id] == playload.user_id:
                    await self.check_for_fishing(playload=playload)

    @commands.Cog.listener()
    async def on_message(self, message):
        global lasttime
        if time.time() - lasttime > 10:
            lasttime = time.time()
            executeSomething()

def setup(bot):
    bot.add_cog(Economy(bot))
