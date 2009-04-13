# Brian Cottingham
# spiffytech@gmail.com
# 2009-04-10
# Various IRC pranks. 

import time
import random

def kill(connection, event, target):
    '''Shouts "die" at someone. Formerly attempted to boot someone with an excess flood'''
    channel = event.target()
    for i in range(0, 3):
        connection.privmsg(channel, "%s, die!" % target)
#        if i % 25 == 0:  #If you really want to flood somebody, make sure you don't get yourself kicked
#            time.sleep(5)



#Roulette variables
random.seed(time.time())
currentBarrel = 7
bulletLoc = random.randint(1, 6)
emptyPhrases = (
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
reloadPhrases = (
    "Who's feelin' lucky?",
    "Hear we go again.",
    "Round and round we go, where it stops, only I know.",
    "Too bad. Maybe this time will turn out better."
)

def roulette(connection, event, args):
    global currentBarrel
    global bulletLoc

    if args == "spin":
        currentBarrel = 7
        bulletLoc = random.randint(1, 6)
        connection.privmsg(event.target(), "*spin*")
        connection.privmsg(event.target(), "Don't like counting chambers, eh?")
        return

    currentBarrel -= 1
    if currentBarrel == bulletLoc:
        connection.privmsg(event.target(), "Bang! %s is dead!" % event.source().split("!")[0])
        currentBarrel = 0
    else:
        connection.privmsg(event.target(), "*click*")
        connection.privmsg(event.target(), random.choice(emptyPhrases))

    if currentBarrel == 0:
        currentBarrel = 7
        bulletLoc = random.randint(1, 6)
        connection.privmsg(event.target(), "RELOAD! *click* *spin*")
        connection.privmsg(event.target(), random.choice(reloadPhrases))
