# MUST BE PYTHON 3.6!!!
import discord
import asyncio
import os
import random

import markov

TOKEN = os.environ.get('DISCORD_BOT_SECRET')

log_file = open('store.txt', 'a')

client = discord.Client()


@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    else:
        log_file = open('store.txt', 'a')
        log_file.write(message.content + '\n')
        log_file.close()

    if message.content.startswith('!rip '):
        print(message.author.id)
        full_command = message.content[message.content.index(' ') + 1:].split(' ')
        print(full_command)
        command = full_command[0]
        # try:
        if command == 'help':
            initial = await client.send_message(message.channel,
            """
help: Displays this very message.\n
roll [#dice]d[value of dice][+/-value]: Rolls dice for random numbers.\n
thanos: Snaps half of all members.\n
\n
THIS MESSAGE WILL SELF DESTRUCT IN 10 SECONDS
            """)
            await asyncio.sleep(10)
            await client.delete_message(initial)

        elif command == 'hello':
            msg = 'Hello {0.author.mention}'.format(message)
            print(message.author)
            print(message.content)
            await client.send_message(message.channel, msg)

        # Rolls dnd dice
        elif command == 'roll':
            dice = full_command[1].lower()
            times = int(dice[:dice.index('d')])
            additive = 0
            if '+' in dice:
                multiple = int(dice[dice.index('d') + 1:dice.index('+')])
                additive = int(dice[dice.index('+'):])
            elif '-' in dice:
                multiple = int(dice[dice.index('d') + 1:dice.index('-')])
                additive = int(dice[dice.index('-'):])
            else:
                multiple = int(dice[dice.index('d') + 1:])
            total = 0
            for i in range(times):
                total += random.randint(1, multiple)

            if additive:
                total += additive
            msg = "{} result: {}".format(dice, total)
            # Special text for d20
            if dice == '1d20' and total == 20:
                msg = "NAT TWENTY!\n" + msg
            if dice == '1d20' and total == 1:
                msg = "NAT ONE!\n" + msg
            await client.send_message(message.channel, msg)

        # Thanos bot
        elif command == 'thanos':
            members = message.server.members
            users = []
            for member in members:
                if not member.bot:
                    users.append(member.name)

            random.shuffle(users)
            msg = ""
            if len(users) == 2 or len(users) == 1:
                msg = ", ".join(users) + " is snapped."
            else:
                msg = "The following members are snapped: " + str(", ".join(users[:len(users) // 2]) + ".")

            await client.send_message(message.channel, msg)

        # except:
        #    await client.send_message(message.channel, "Ouch oof owie my syntax")

        elif command == 'emote':
            emoji = full_command[1]

            msg = ':{}:'.format(emoji)
            await client.send_message(message.channel, msg)

        elif command == 'generate' and message.author.id == "183384474095058944":
            await client.send_message(message.channel, markov.generate())
    else:
        prevword = None
        for word in message.content.split():
            # print(word)
            markov.add_word(prevword, word)
            prevword = word
        markov.add_word(prevword, None)
        # await client.send_message(message.channel, markov.generate())

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
