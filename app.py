# MUST BE PYTHON 3.6!!!
import discord
import asyncio
import os
import random

from discord.ext import commands

import markov

TOKEN = os.environ.get('DISCORD_BOT_SECRET')

prefix = "!rip "

bot = commands.Bot(command_prefix=prefix)

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


@bot.group()
async def config(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("No command sent...")


@config.command()
async def thanos(ctx):
    await ctx.send("Thanos snaps half of the members in the server.")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.content.startswith(prefix):
        await bot.process_commands(message)
    else:
        prevword = None
        for word in message.content.split():
            # print(word)
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
            await message.channel.send("Hi '" + dad_joke + "', I'm dad.")

bot.run(TOKEN)
