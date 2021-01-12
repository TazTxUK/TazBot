import discord
import typing
from typing import Dict, Tuple, Callable
import traceback
import json
import asyncio
import lupa

runtime_lua = lupa.LuaRuntime(unpack_returned_tuples=True)
prefix = "[]"

with open("private/token.json") as f:
    token = json.load(f)["token"]

global client
client = discord.Client(chunk_guilds_at_startup=True, intents = discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message_delete(msg):
    await client.get_channel(784527120323838012).send("**DELETED MESSAGE**\nSender: " + msg.author.name + "\nContent:\n" + msg.content)

admins = [
    "179652150710763520",
    "179967331336716289",
    "179651817762717696"
]

commands : Dict[str, Callable] = {}
reporting_channel : discord.TextChannel = client.get_channel(784527120323838012)

@client.event
async def on_message(message : discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith("[py]"):
        val = eval(message.content[4:])
        await message.channel.send(str(val))
        return

    if message.content.startswith("[lua]"):
        import lua
        c = message.content[5:]
        val = lua.runtime.execute(c)
        await message.channel.send(str(val))
        return

    if message.content.startswith(prefix):
        msg = message.content[len(prefix):]
        com = msg.split(" ")
        if (com[0] in commands):
            try:
                asyncio.create_task(commands[com[0]](message, com))
            except Exception as e:
                tb = traceback.format_exc()
                await reporting_channel.send("```py\n"+tb+"\n```")
        else:
            await message.channel.send("Unknown command.")

def register_command(str, fn):
    print("registered command - " + str)
    commands[str] = fn

def run():
    client.run(token)