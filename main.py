import discord

import bot
from typing import List

async def com_ping(message : discord.Message, com : List[str]):
    await message.channel.send(f"The bot responded in {round(bot.client.latency * 1000)}ms")

async def com_users(message : discord.Message, com : List[str]):
    s = ""
    for user in bot.client.users:
        s += user.name + " " + str(user.id) + "\n"
    await message.channel.send(s)

async def com_guilds(message : discord.Message, com : List[str]):
    s = ""
    async for guild in bot.client.fetch_guilds(limit=150):
        s += guild.name + "\n"
    await message.channel.send(s)

async def com_exec(message : discord.Message, com : List[str]):
    pass

async def com_help(message : discord.Message, com : List[str]):
    s = "***COMMANDS:***\n"
    for cmd in bot.commands:
        s += "[]" + cmd + "\n"
    await message.channel.send(s)

bot.register_command("ping", com_ping)
bot.register_command("users", com_users)
bot.register_command("servers", com_guilds)
bot.register_command("exec", com_exec)
bot.register_command("help", com_help)

bot.run()

'''
async def onM(message):
    if message.author == client.user:
        return

    if message.content.startswith("[]"):
        msg = message.content[2:]
        com = msg.split(" ")
        if com[0] == "image":
            async with message.channel.typing():
                os.chdir("C:/Users/tazst/Pictures")
                types = ("*.png", "*.jpg", "*.PNG", "*.jpeg")
                files = []
                for file in types:
                    files.extend(glob.glob(file))
                
                await message.channel.send("",file=discord.File("C:/Users/tazst/Pictures/" + random.choice(files)))
        elif com[0] == "stats":
            user = None
            try:
                for member in message.guild.members:
                    if com[1] in member.name:
                        user = member
                        break
            except IndexError:
                user = None

            if user is None:
                user = message.author

            s = "**Stats for " + user.name + ":**"
            s += "\nSTRENGTH: " + str(random.randint(0,10)*10)
            s += "\nDEFENSE: " + str(random.randint(0,10)*10)
            s += "\nAGILITY: " + str(random.randint(0,10)*10)
            s += "\nAIM: " + str(random.randint(0,10)*10)

            await message.channel.send(s)
        elif com[0] == "hg":
            await message.channel.send(hg.readCommandArgs(message, com[1:]))
            hg.saveJson()
        #elif com[0] == "scheduletest":
        #    ac = schedule.lads[com[1]].getActivity(datetime.datetime(2020,12,8 + int(com[2]),int(com[3]),int(com[4]),0,0))
        #    await message.channel.send(str(ac))
        elif com[0] == "scheduletest":
            if com[1] not in schedule.lads:
                await message.channel.send("Input a name as the first argument. eg " + random.choice(list(schedule.lads.keys())))
                return

            date = datetime.date.today()
            for c in com[2:]:
                low = c[:2].lower()
                if low in schedule.daymap:
                    wday = schedule.daymap[low]
                    date += datetime.timedelta(days=(wday - date.weekday() - 1) % 7 + 1)
                    break

            time_str = next((s for s in com[2:] if ":" in s), None)
            time = None
            if time_str == None:
                await message.channel.send("Input a 24-hr time. eg 15:00")
                return
            else:
                time = datetime.datetime.strptime(time_str, "%H:%M").time()

            ac = schedule.lads[com[1]].getActivity(datetime.datetime.combine(date, time))
            await message.channel.send(str(ac))
        elif com[0] == "whosfree":
            date = None
            time = None
            if len(com) == 1:
                date = datetime.date.today()
                time = datetime.datetime.now().time()
            else:
                date = datetime.date.today()
                for c in com[1:]:
                    low = c[:2].lower()
                    if low in schedule.daymap:
                        wday = schedule.daymap[low]
                        date += datetime.timedelta(days=(wday - date.weekday()) % 7)
                        break

                time_str = next((s for s in com[1:] if ":" in s), None)
                time = None
                if time_str == None:
                    await message.channel.send("Input a 24-hr time. eg 15:00")
                    return
                else:
                    time = datetime.datetime.strptime(time_str, "%H:%M").time()

                if date == datetime.date.today() and time < datetime.datetime.now().time():
                    date += datetime.timedelta(days=7)

            await message.channel.send(str(date) + " " + str(time))
            await message.channel.send(schedule.getNextFreePeriods(datetime.datetime.combine(date, time)))
        elif com[0] == "updatetimetable":
            async with message.channel.typing():
                schedule.updateRotations()
                schedule.updateLads()
                await message.channel.send("Done.")
        elif com[0] == "react":
            await message.add_reaction("➡️")
        elif com[0] == "battle":
            if len(com) == 1:
                await message.channel.send("Missing second argument.")
            elif com[1] == "addpersons":
                if len(com) == 2:
                    await message.channel.send("Missing third argument.")
                else:
                    battle.add_person(com[2])
            elif com[1] == "listpersons":
                await message.channel.send("**Persons:** " + ", ".join([x.name for x in battle.persons]))
        elif com[0] == "encrypt":
            await encrypt.on_command(message, com[1:])
        elif (com[0] == "chadtest"):
            u = []
            for user in message.guild.members:
                if not user.bot:
                    u.append(user)
            random.shuffle(u)
            await message.channel.send("The virgin " + u[0].name + " versus the chad " + u[1].name)
        elif (com[0] == "superhot"):
            u = []
            for user in message.guild.members:
                if not user.bot:
                    u.append((user, random.randint(0,10)*10))
            s = "**Who is the hottest of them all?**\n"
            u.sort(key=lambda tup: -tup[1])
            for k in u:
                s += k[0].name + ": " + str(k[1]) + "%\n"
            await message.channel.send(s)
        elif (com[0] == "opinion"):
            id = message.author.id
            adj = random.choice(adjs)
            await message.channel.send("My opinion on you, " + (message.author.name) + ", is that you " + adj + ".")
            


'''