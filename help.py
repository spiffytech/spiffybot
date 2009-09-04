#This file is part of Spiffybot.
#
#Spiffybot is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Spiffybot is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Spiffybot.  If not, see <http://www.gnu.org/licenses/>.


commands = {
    "calc": "calc EQUATION: Performs calculations using Google's calculator",
    "encode": "encode STRING: Encodes a string with Morse Code",
    "decode": "MORSE STRING: Decodes a Morse Code string",
    "fact": "Returns a random fact",
    "roulette": "Randomly tries to shoot you, a la Russian Roulette",
    "tell ": "tell PERSON MESSAGE [at TIME]: Delivers a message to a user, either when they next are seen, or at a specific time",
    "tiny": "tiny URL: Returns a tinyurl-encoded url",
    "topics": "topics [N]: Lists the previous n topics",
    "weather": "weather CITY, STATE: Tells you the current weather at a given location",
    "woot": "Returns the current deal on woot.com, it's price, availability, and purchase URL",
}


def help(event):
    if event.args == "":
        cmds = sorted(commands.keys())
        cmds = "Commands: " + ", ".join(cmds)
        event.reply(cmds)
        return
    elif event.args in commands:
        event.reply(commands[event.args])
        return
    else:
        event.reply("You fail at : No such command")
