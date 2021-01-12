
import json

actor_pool = {}

def saveJson():
    with open("data/hg/actor_pool.json","w") as f:
        json.dump(actor_pool, f, indent=4)

def loadJson():
    try:
        with open("data/hg/actor_pool.json","r") as f:
            actor_pool.update(json.load(f))
    except FileNotFoundError:
        print("(hg file not found)")

def newActor(name):
    d = {}
    actor_pool[name] = d
    return d

def getActor(name):
    if name in actor_pool:
        return actor_pool[name]
    else:
        return None

def getActorName(actor):
    if "nickname" in actor:
        return actor["nickname"]
    elif "forename" in actor:
        if "surname" in actor:
            return actor["forename"] + " " + actor["surname"]
        else:
            return actor["forename"]
    elif "surname" in actor:
        return actor["surname"]
    else:
        return None

def readCommandArgs(message, com, offset = 0, charid = None, char = None):
    s = ""
    if com[offset] == "newid":
        charid = com[offset + 1]
        char = newActor(com[offset + 1])
        s += "Adding char id " + com[offset + 1] + "\n"
        offset += 2
    elif com[offset] == "id":
        charid = com[offset + 1]
        char = getActor(com[offset + 1])
        if char is None:
            s += "No character with that ID exists."
        else:
            s += "Modifying char id " + com[offset + 1] + "\n"
        offset += 2
    elif com[offset] == "forename":
        if not char is None:
            char["forename"] = com[offset + 1]
            s += "Set forename to " + com[offset + 1] + "\n"
        offset += 2
    elif com[offset] == "surname":
        if not char is None:
            char["surname"] = com[offset + 1]
            s += "Set surname to " + com[offset + 1] + "\n"
        offset += 2
    elif com[offset] == "nickname":
        if not char is None:
            char["nickname"] = com[offset + 1]
            s += "Set nickname to " + com[offset + 1] + "\n"
        offset += 2
    elif com[offset] == "discord_user_id":
        if not char is None:
            char["discord_user"] = int(com[offset + 1])
            s += "Set discord id to " + com[offset + 1] + "\n"
        offset += 2
    elif com[offset] == "is":
        if not char is None:
            if com[offset + 1] == "here":
                user = None
                for member in message.guild.members:
                    if charid.replace(" ", "").lower() in member.name.replace(" ", "").lower():
                        user = member
                        break
                
                if user == None:
                    s += "No appropriate user found for " + charid + "\n"
                else:
                    char["discord_user"] = user.id
                    s += "Set discord id to " + str(user.id) + "\n"
            elif not com[offset + 1].isnumeric():
                user = None
                for member in message.guild.members:
                    if com[offset + 1].replace(" ", "").lower() in member.name.replace(" ", "").lower():
                        user = member
                        break
                
                if user == None:
                    s += "No appropriate user found for " + com[offset + 1] + "\n"
                else:
                    char["discord_user"] = user.id
                    s += "Set discord id to " + str(user.id) + "\n"
            else:
                char["discord_user"] = int(com[offset + 1][3:-1])
                s += "Set discord id to " + com[offset + 1][3:-1] + "\n"
        offset += 2
    # elif com[offset] == "tags":
    #     tags_added = ""
    #     if not char is None:
    #         while com[offset + 1] != "end":
    #             tags_added += com[offset + 1] + ", "
    #             addTag(char, com[offset + 1])
    #             offset += 1
    #     s += "Added tags " + tags_added[:-2]
    #     offset += 1
    elif com[offset] == "list":
        actors = ""
        for actor in actor_pool:
            name = getActorName(actor_pool[actor])
            if name is None:
                name = actor
            actors += name + ", "
        s += "Actors: " + actors[:-2]
        offset += 1
    else:
        s += "Unknown subcommand " + com[offset] + "\n"
        offset += 1

    if offset < len(com):
        s += readCommandArgs(message, com, offset, charid, char)

    return s

