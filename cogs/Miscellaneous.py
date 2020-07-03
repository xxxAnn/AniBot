import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
from Libraries.Library import get_guild_language
import time

class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['setlang'])
    @has_permissions(administrator=True)
    async def set_language(self, ctx, language_code):
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
            content[str(ctx.guild.id)] = {"Language": language_code}
            d = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
            with open("data/settings.json", "w") as file:
                file.write(d)
            language = get_guild_language(ctx.guild.id)
            await ctx.send(local[1][language])

    @commands.command(pass_context=True)
    async def members(self, ctx, rolename: discord.Role):
        local = [{'en': 'Members', 'ja': 'ロールのメンバー', "fr": "Membre"}, {'en': 'in ', 'fr': 'de ', 'ja': 'ロール：'}]
        language = get_guild_language(ctx.guild.id)
        mm = ctx.message.guild.members
        embed = discord.Embed(title=local[0][language], description=local[1][language] + str(rolename), color=0x0d20a4)
        for tm in mm:
            if rolename in tm.roles:
                embed.add_field(name=tm.display_name, value=tm.mention, inline=True)
        await ctx.send(embed=embed)

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

    @commands.command(pass_context=True)
    async def react(self, ctx, arg):
        msg = ctx.message
        await msg.add_reaction(arg)
        x = await ctx.send(arg)
        time.sleep(0.2)
        await x.delete()
        print(arg)

    @commands.command()
    async def online(self, ctx):
        local = [
        {'en': "Online", 'fr': "En ligne", 'ja': "オンライン"},
        {'en': "Shows a list of online members", 'fr': "Montre la liste des membres en ligne", 'ja': "オンラインメンバーを見せる"},
        {'en': "Online members:", 'fr': "Membre en ligne:", 'ja': "オンラインメンバー"}
        ]
        language = get_guild_language(ctx.guild.id)
        mem = ctx.message.guild.members
        embed = discord.Embed(title=local[0][language], description=local[1][language], color=0x0d20a4)
        temp = ""
        for i in mem:
            k = str(i.status)
            if k == "online" or k == "idle" or k == "dnd":
                if not i.bot:
                    temp+=i.mention+"\n"
        embed.add_field(name=local[2][language], value=temp, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discord.com/oauth2/authorize?client_id=705502515491242014&scope=bot&permissions=322630")

    @commands.command(aliases=['8ball'])
    async def question(self, ctx, *, arg):
        y = ["yes", "no", "probably", "definitely not", "ofc not?", "you'll soon know", "definitely"]
        x = random.choice(y)
        await ctx.send(x)

    @commands.command(pass_context=True)
    async def oldest(self, ctx):
        list_ids = []
        local = [
        {'en': " is the oldest member of the guild", 'fr': " est le member le plus vieux de la guilde", 'ja': "さんは鯖の最年長メンバーであります"},
        ]
        language = get_guild_language(ctx.guild.id)
        smallest = 999999999999999999999
        for i in ctx.guild.members:
            if i.id < smallest and i.bot is False:
                smallest = i.id
        await ctx.send(ctx.guild.get_member(smallest).display_name + local[0][language])


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
