# Brian Cottingham
# spiffytech@gmail.com
# 2009-05-07
# Plays Russian Roulette

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

import time
import random

channels = {}

def roulette(connection, event, args):
    '''Plays Russian Roulette. When finished, will try to kick a nick from the channel when hit.'''
    if not event.target() in channels:
        channels[event.target()] = channel()
    c = channels[event.target()]
    if args == "spin":
        c.spin(connection, event)
    else:
        c.shoot(connection, event)



class channel():
    def __init__(self):
        #Roulette variables
        random.seed(time.time())
        self.currentBarrel = 7
        self.bulletLoc = random.randint(1, 6)
        self.emptyPhrases = (
            "No bullet here",
            "Empty chamber",
            "You didn't really think that was going to work, did you?",
            "Miss!",
            "Try again!",
            "You fail at guns",
            "n chamber(s) down, (6-n) to go!",
            "Come on, pull that trigger like you mean it!",
            "Maybe another spin would help",
        )
        self.reloadPhrases = (
            "Who's feelin' lucky?",
            "Hear we go again.",
            "Round and round we go, where it stops, only I know.",
            "Too bad. Maybe this time will turn out better."
        )

    def spin(self, connection, event):
        self.currentBarrel = 7
        self.bulletLoc = random.randint(1, 6)
        connection.privmsg(event.target(), "*spin*")
        connection.privmsg(event.target(), "Don't like counting chambers, eh?")

    def shoot(self, connection, event):
        self.currentBarrel -= 1
        if self.currentBarrel == self.bulletLoc:
            connection.privmsg(event.target(), "Bang! %s is dead!" % event.source().split("!")[0])
            self.currentBarrel = 0
        else:
            connection.privmsg(event.target(), "*click*")
            connection.privmsg(event.target(), random.choice(self.emptyPhrases))

        if self.currentBarrel == 0:
            self.currentBarrel = 7
            self.bulletLoc = random.randint(1, 6)
            connection.privmsg(event.target(), "RELOAD! *click* *spin*")
            connection.privmsg(event.target(), random.choice(self.reloadPhrases))
