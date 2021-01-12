
from typing import List
import discord
from cryptography.fernet import Fernet
import asyncio

fern = None

async def on_command(message : discord.Message, com : List[str]):
    global key
    if com[0] == "genkey":
        key = Fernet.generate_key()
        fern = Fernet(key)
        await message.channel.send(key.decode("ascii") + "\nKey set.")
    elif com[0] == "setkey":
        try:
            key = com[1].encode("ascii")
            fern = Fernet(key)
            await message.channel.send("Key set.")
        except IndexError:
            await message.channel.send("Please enter a key.")
        except:
            await message.channel.send("Invalid key.")
    elif com[0] == "encode":
        m = " ".join(com[1:])
        fern = Fernet(key)
        await message.channel.send("Key set.")


