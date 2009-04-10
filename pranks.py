# Brian Cottingham
# spiffytech@gmail.com
# 2009-04-03
# Contains various IRC pranks. 

from time import sleep

def kill(irc, event, target):
    '''Attempts to boot someone with an excess flood'''
    channel = event.target()
    for i in range(0, 3):
        irc.privmsg(channel, "%s, die!" % target)
        if i % 25 == 0:
            sleep(5)

#def roulette(irc, channel, sender)
