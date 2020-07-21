import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
from Libraries.Library import get_guild_language, Pages, command_activated, embed_template
import time
import inspect

class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['setlang'])
    @has_permissions(administrator=True)
    async def set_language(self, ctx, language_code):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        language_code = str.lower(language_code)
        available_languages = ['fr', 'en', 'ja']
        local = [
        {'en': "Please use 'fr', 'en' or 'ja'", 'fr': "Utiliser 'fr', 'en' ou 'ja' comme argument", "ja": "引数は「fr」か「en」か「ja」なければいけない。"},
        {'en': "Successfully changed language", 'fr': "Changement de langue réussi", 'ja': '言語変更成功しました'}
        ]
        language = get_guild_language(ctx.guild.id)
        if language_code not in available_languages:
            await ctx.send(local[0][language])
        else:
            with open("data/settings.json", "r") as f:
                x = f.read()
                content = json.loads(x)
                f.close()
            content[str(ctx.guild.id)]['Language'] = language_code
            d = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
            with open("data/settings.json", "w") as file:
                file.write(d)
            language = get_guild_language(ctx.guild.id)
            embed = await embed_template("Set Language", local[1][language])
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def members(self, ctx, rolename: discord.Role):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        local = [{'en': 'Members', 'ja': 'ロールの全員', "fr": "Membre"}, {'en': 'in ', 'fr': 'de ', 'ja': 'ロール：'}]
        language = get_guild_language(ctx.guild.id)
        mm = ctx.message.guild.members
        list = []
        for member in mm:
            if member in rolename.members:
                list.append(member.mention)
        page = Pages(ctx=ctx, entries=list, custom_title=local[0][language])
        await page.paginate()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("data/settings.json", "r") as f:
            x = f.read()
            content = json.loads(x)
            f.close()
        content[str(guild.id)] = {"Language": "en"}
        d = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
        with open("data/settings.json", "w") as file:
            file.write(d)
        JOIN_LOG_CHANNEL = self.bot.get_channel(734863274352574465)
        embed=discord.Embed(title="Guild joined", description="{}".format(guild.name), color=0x1ad58e)
        embed.add_field(name="Guild Members", value="{}".format(len(guild.members)), inline=False)
        embed.set_footer(text="🎉")
        await JOIN_LOG_CHANNEL.send(embed=embed)

    @commands.command(pass_context=True)
    async def react(self, ctx, arg):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        msg = ctx.message
        await msg.add_reaction(arg)
        x = await ctx.send(arg)
        time.sleep(0.2)
        await x.delete()
        print(arg)

    @commands.command()
    @has_permissions(administrator=True)
    async def add_reaction_role(self, ctx, message_id: int, channel: discord.TextChannel, role: discord.Role, reaction):
        if not await command_activated(ctx, 'add_reaction_role'): return
        message = await channel.fetch_message(message_id)
        await message.add_reaction(reaction)
        with open('data/reactionroles.json', 'r') as file:
            x = file.read()
            content = json.loads(x)
        if str(message_id) not in content:
            content[str(message_id)] = {reaction: role.id}
        else:
            content[str(message_id)][reaction] = role.id
        with open('data/reactionroles.json', 'w') as file:
            x = json.dumps(content)
            file.write(x)
        await ctx.send("Succesfully added role react, make sure the bot has sufficient permissions or this will not work")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, playload):
        with open('data/reactionroles.json', 'r') as file:
            x = file.read()
            content = json.loads(x)
        if str(playload.message_id) in content:
            print(playload.emoji)
            if str(playload.emoji) in content[str(playload.message_id)]:
                await playload.member.add_roles(self.bot.get_guild(playload.guild_id).get_role(content[str(playload.message_id)][str(playload.emoji)]))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, playload):
        with open('data/reactionroles.json', 'r') as file:
            x = file.read()
            content = json.loads(x)
        if str(playload.message_id) in content:
            print(playload.emoji)
            if str(playload.emoji) in content[str(playload.message_id)]:
                await self.bot.get_guild(playload.guild_id).get_member(playload.user_id).remove_roles(self.bot.get_guild(playload.guild_id).get_role(content[str(playload.message_id)][str(playload.emoji)]))

    @commands.command()
    async def online(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        local = [
        {'en': "Online", 'fr': "En ligne", 'ja': "オンライン"},
        {'en': "Shows a list of online members", 'fr': "Montre la liste des membres en ligne", 'ja': "オンラインメンバーを見せる"},
        {'en': "Online members:", 'fr': "Membre en ligne:", 'ja': "オンラインメンバー"}
        ]
        language = get_guild_language(ctx.guild.id)
        mem = ctx.message.guild.members
        temp = []
        for i in mem:
            k = str(i.status)
            if k == "online" or k == "idle" or k == "dnd":
                if not i.bot:
                    temp.append(i.mention)
        page = Pages(ctx, entries=temp, custom_title=local[0][language])
        await page.paginate()

    @commands.command()
    @has_permissions(administrator=True)
    async def toggle_command(self, ctx, command_name: str):
        on=await command_activated(ctx, str.lower(command_name), verbose=False)
        with open('data/settings.json', 'r') as file:
            content = file.read()
            settings = json.loads(content)
        if on:
            settings[str(ctx.guild.id)]["command_permissions"][str.lower(command_name)] = False
        elif not on:
            settings[str(ctx.guild.id)]["command_permissions"][str.lower(command_name)] = True
        d = json.dumps(settings, sort_keys=True, indent=4, separators=(',', ': '))
        with open("data/settings.json", "w") as file:
            file.write(d)
        embed = await embed_template("Toggle command", "Command was successfully toggled")
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        embed = await embed_template("Invite", "[Click here to add the bot to your server](https://discord.com/oauth2/authorize?client_id=705502515491242014&scope=bot&permissions=322630)")
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball'])
    async def question(self, ctx, *, arg):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        y = ["yes", "no", "probably", "definitely not", "ofc not?", "you'll soon know", "definitely"]
        x = random.choice(y)
        embed = await embed_template("Question", x)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def oldest(self, ctx):
        if not await command_activated(ctx, str(inspect.stack()[0][3])): return
        list_ids = []
        local = [
        {'en': " is the oldest member of the guild", 'fr': " est le member le plus vieux de la guilde", 'ja': "さんは鯖の最年長メンバーであります"},
        ]
        language = get_guild_language(ctx.guild.id)
        smallest = 999999999999999999999
        for i in ctx.guild.members:
            if i.id < smallest and i.bot is False:
                smallest = i.id
        embed = await embed_template("Oldest", ctx.guild.get_member(smallest).display_name + local[0][language])
        await ctx.send(embed=embed)

    @commands.command()
    async def privacy_policy(self, ctx):
        text = "**__Privacy Policy__** \r\nAbsolutely no information other than snowflake ids provided by the guild will be saved, those snowflake ids are encrypted and secure in a database protected through SSH. Any violation of privacy will be promptly reported to the client. \r\n**__Contact__**\r\nIf you have any concerns or questions contact me at amehikoji@gmail.com."
        await ctx.send(text)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
