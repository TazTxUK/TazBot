import discord
import typing
from typing import Dict, Tuple, Callable
import traceback
import json
import asyncio
from discord.channel import TextChannel
import lupa
import pyduktape

runtime_lua = lupa.LuaRuntime(unpack_returned_tuples=True)
runtime_js = pyduktape.DuktapeContext()

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
        await message.channel.send(str(val)[:2000])
        return

    if message.content.startswith("[lua]"):
        c = message.content[5:]
        val = runtime_lua.execute(c, message)
        await message.channel.send(str(val)[:2000])
        return

    if message.content.startswith("[js]"):
        runtime_js.set_globals(message=message)
        c = message.content[4:]
        val = runtime_js.eval_js(c)
        await message.channel.send(str(val)[:2000])
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
    commands[str] = asyncio.coroutine(fn)

def lua_create_task(coro):
    asyncio.create_task(coro)

globals_lua = runtime_lua.globals()
globals_lua["register_command"] = register_command
globals_lua["bot"] = globals()
globals_lua["asyncio"] = asyncio

runtime_js.set_globals(
    register_command=register_command,
    bot=globals(),
    asyncio=asyncio
)

def run():
    client.run(token)

import os
import importlib

for filename in os.listdir("autoload"):
    if filename.endswith(".py"):
        print("python import: " + filename)
        importlib.import_module("autoload." + filename[:-3])
    elif filename.endswith(".lua"):
        print("lua import: " + filename)
        runtime_lua.require("autoload." + filename[:-4])
    elif filename.endswith(".js"):
        print("js import: " + filename)
        runtime_js.eval_js_file("autoload/" + filename[:-3])
    else:
        print("ignored " + filename)