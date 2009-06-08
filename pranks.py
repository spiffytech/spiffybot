# Brian Cottingham
# spiffytech@gmail.com
# 2009-04-10
# Various IRC pranks

import time
import random

channels = {}

def kill(connection, event, target):
    '''Shouts "die" at someone. Formerly attempted to boot someone with an excess flood'''
    channel = event.target()
    for i in range(0, 3):
        connection.privmsg(channel, "%s, die!" % target)
#        if i % 25 == 0:  #If you really want to flood somebody, make sure you don't get yourself kicked
#            time.sleep(5)



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
