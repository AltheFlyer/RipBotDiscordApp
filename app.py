# MUST BE PYTHON 3.6!!!
import discord
import asyncio
import os
import random

from discord.ext import commands

import markov

# You must have this set to a valid discord bot secret!
# Note windows can be slow/sucky so if may not work immediately :/
TOKEN = os.environ.get('DISCORD_BOT_SECRET')

prefix = "!rip "
default_configs = {"dadword": "dad"}
servers = {}
bot = commands.Bot(command_prefix=prefix, help_command=None)


async def is_mod(ctx):
    return ctx.message.author.permissions_in(ctx.message.channel).manage_guild


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Advanced Fun'))


@bot.command()
async def thanos(ctx):
    names = [member.name for member in ctx.guild.members]
    random.shuffle(names)

    last = names[int(len(names)/2) - 1]
    names = names[0:int(len(names)/2) - 1]
    output = ", ".join(names)

    if len(names) == 0:
        output = last + " has been snapped!"
    elif len(names) == 1:
        output = ", ".join(names) + " and " + last + " have been snapped!"
    elif len(names) > 1:
        output = ", ".join(names) + ", and " + last + " have been snapped!"

    await ctx.send(output)


@bot.command()
async def generate(ctx):
    await ctx.send(markov.generate())


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Ripbot", url="https://www.google.com", description="An almost entertaining bot.",
                          color=0xffffff)
    embed.set_author(name="Ripbot-Help")
    embed.add_field(name="Commands", value="thanos, generate", inline=False)
    embed.add_field(name="Passive", value="Dad Responses,  Markov Builder", inline=False)
    embed.set_footer(text="(Check it out on Github)")
    await ctx.send(embed=embed)


@bot.group()
@commands.check(is_mod)
async def config(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("No command sent...")


@config.error
async def config_error(ctx, error):
    if commands.CheckFailure:
        await ctx.send("You don't have the permissions to use that command!")


@config.command()
async def thanos(ctx):
    await ctx.send("Thanos snaps half of the members in the server.")


@config.command()
async def setvalue(ctx, arg1, *, args):
    if arg1 in configs:
        configs[arg1] = args
        await ctx.send("Config successfully changed: " + arg1 + " -> " + args)
    else:
        await ctx.send("Could not find specified config.")


@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return
    elif message.content.startswith(prefix):
        # Check for bot prefix, run command suite if present
        await bot.process_commands(message)
    else:
        # Markov storage
        prevword = None
        for word in message.content.split():
            markov.add_word(prevword, word)
            prevword = word
        markov.add_word(prevword, None)

        # Colin features
        checks = ["im", "I'm", "IM", "i am", "I am", "I AM"]
        im_index = -1
        for term in checks:
            if term in message.content:
                im_index = message.content.rindex(term) + len(term) + 1

        if im_index > -1:
            print("A")
            dad_joke = message.content[im_index:]
            await message.channel.send("Hi '" + dad_joke + "', I'm " + configs["dadword"] + ".")


bot.run(TOKEN)
