import discord
from discord.ext import commands
import asyncio
import random
import json
import os

discord_app_token = "YOUR TOKEN HERE"
commandSign = "*" # Sign to use at the start of a command (1 character only)
commands = "ping, addquote, quote, help"
help_text = "Hi, I'm SUGAR! I can do fun tricks. \n \nMy commands are: \n" + commands + ". \nAdd a " + commandSign \
            + " to the beginning to use them."
client = discord.Client()

if not os.path.isfile("help_file.txt"):
    with open("help_file.txt", "w") as help_file:
        json.dump(help_text, help_file)
else:
    with open("help_file.txt", "r") as help_file:
        help_text = json.load(help_file)

async def game_changer():
    if not os.path.isfile("game_file.pkl"):
        game_list = ["nothing","something","everything"]
    else:
        with open("game_file.txt", "r") as game_file:
            game_list = json.load(game_file)
    with open("game_file.txt", "w") as game_file:
        json.dump(game_list, game_file)
    await client.wait_until_ready()
    while not client.is_closed:
        for game in game_list:
            name_of_the_game = game
            await client.change_presence(game=discord.Game(name=name_of_the_game))
            await asyncio.sleep(300)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith(str(commandSign)):
        if message.content.startswith("ping",1):
            await client.send_message(message.channel, "Pong.")
        elif message.content.startswith("addquote",1):
            if not os.path.isfile("quote_file.txt"):
                quote_list = []
            else:
                with open("quote_file.txt", "r") as quote_file:
                    quote_list = json.load(quote_file)
            quote_list.append(message.content[9:])
            with open("quote_file.txt", "w") as quote_file:
                json.dump(quote_list, quote_file)
        elif message.content.startswith("quote",1):
            with open("quote_file.txt", "r") as quote_file:
                quote_list = json.load(quote_file)
            await client.send_message(message.channel, random.choice(quote_list))
        elif message.content.startswith("help",1):
            await client.send_message(message.channel, help_text)

client.loop.create_task(game_changer())
client.run(discord_app_token)