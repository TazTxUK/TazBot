import bot
import discord
from typing import List

async def com_pyexample(message : discord.Message, com : List[str]):
    await message.channel.send("Python example runs successfully!")

bot.register_command("pyexample", com_pyexample)