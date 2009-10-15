# Miscelaneous commands that don't really fit anywhere else

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

import random
import cPickle as pickle
import re
from sqlite3 import dbapi2 as sqlite
import time

dbName = "logs.db"

def trivia(event):
    '''Responds with a random trivial fact'''
    trivia = pickle.load(open("misc/trivia.pickle"))
    random.seed(time.time())
    fact = random.choice(trivia)
    print "Replying in channel" + event.channel
    event.reply(fact)



def excuse(event):
    '''Responds with a random excuse'''
    excuses = pickle.load(open("misc/excuses.pickle"))
    random.seed(time.time())
    excuse = random.choice(excuses)
    print "Replying in channel" + event.channel
    event.reply(excuse)



def farewell(event):
    '''When a user says "bye", respond with a fancy farewell message'''
    farewells = pickle.load(open("misc/farewells.pickle"))
    random.seed(time.time())
    message = random.choice(farewells)
    print "Replying in channel" + event.channel
    event.reply(message)



def threeCheers(event):
    random.seed(time.time())
    cheers = ["hurrah", "hooray", "huzzah",]
    cheer = random.choice(cheers)
    
    for i in range(3):
        event.reply(cheer + " for " + event.args)
        time.sleep(1.1)



def difficultyCheck(event):
    diffs = {
        "very easy": 0,
        "easy": 5,
        "average": 10,
        "tough": 15,
        "challenging": 20,
        "formidable": 25,
        "heroic": 30,
        "nearly impossible": 40
    }
    if event.args == "":
        limit = diffs["average"]
    else:
        try:
            limit = diffs[event.args]
        except:
            event.reply("No such difficulty level. You fail at seeing if you fail.")
            return

    random.seed(time.time())
    roll = random.randint(1, 20)
    if roll >= limit:
        event.reply("Victory! You roll a %d, requiring only a %d" % (roll, limit))
    else:
        event.reply("You fail at your challenge with a roll of %d out of %d!" % (roll, limit))


def roll_dice(event):
    random.seed(time.time())
    if event.args == "":
        roll = random.randint(1, 6)
        event.reply("%s: your roll was a %d" % (event.sender, roll))
        return

    dice = re.match("(?P<count>[1-9][0-9]*)d-*(?P<die_type>[1-9][0-9]*)(\+(?P<modifier>[0-9]+){1})*.*", event.args)
    if dice == None:
        event.reply("That's not a real dice type!")
        return
    dice = dice.groupdict()
    die_count = int(dice["count"])
    die_type = int(dice["die_type"])
    if dice["modifier"] != None:
        modifier = int(dice["modifier"])

    roll = 0
    for i in range(die_count):
        roll += random.randint(1, die_type)
    if "modifier" in locals():
        roll += modifier

    event.reply("%s You rolled a %d" % (event.sender, roll))
