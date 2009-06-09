commands = {
    "calc": "calc EQUATION: Performs calculations using Google's calculator",
    "encode": "encode STRING: Encodes a string with Morse Code",
    "decode": "MORSE STRING: Decodes a Morse Code string",
    "fact": "Returns a random fact",
    "roulette": "Randomly tries to shoot you, a la Russian Roulette",
    "tell ": "tell PERSON MESSAGE [at TIME]: Delivers a message to a user, either when they next are seen, or at a specific time",
    "tiny": "tiny URL: Returns a tinyurl-encoded url",
    "topics": "topicd [N]: Lists the previous n topics",
    "weather": "weather CITY, STATE: Tells you the current weather at a given location",
    "woot": "Returns the current deal on woot.com, it's price, availability, and purchase URL",
}


def help(connection, event, args):
    type(args)
    print args
    if args == "":
        cmds = sorted(commands.keys())
        cmds = "Commands: " + ", ".join(cmds)
        connection.privmsg(event.target(), cmds)
        return

    elif args in commands:
        connection.privmsg(event.target(), commands[args])
        return
    else:
        connection.privmsg(event.target(), "You fail at : No such command")
