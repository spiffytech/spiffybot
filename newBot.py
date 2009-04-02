#!/usr/bin/env python

import irclib

# Connection information
network = 'irc.freenode.net'
port = 6667
channel = '#bottest'
nick = 'spiffybot'
realName = 'spiffybot'


commands = {}
execfile("commands.py")


def main():

    # Create an IRC object
    irc = irclib.IRC()
#    irclib.DEBUG = True

    # Create a server object, connect and join the channel
    server = irc.server()
    server.connect(network, port, nick, ircname = realName)
    server.join(channel)

    # Add event handlers
    irc.add_global_handler("pubmsg", gotMessage)
    irc.add_global_handler("privmsg", gotMessage)

    # Jump into an infinite loop
    irc.process_forever()



def gotMessage(connection, event):
    '''Someone sent a message to a channel!'''
    sender = event.source().split("!")[0]  # Who sent the message
    message = event.arguments()[0].split()  # What was the message?
    if message[0].startswith(nick):  # If it's a command for us:
        command = message[1]
        args = " ".join(message[2:])  # Quite unexplainably, this will never throw an index-out-of-range error
        try:  # See if we have a command in our list to match what the user told us to do
            if args != "":  # Not all commands take arguments
                reply = commands[command](args)
            else:
                reply = commands[command]()
        except KeyError:
            reply = "Maybe."

        connection.privmsg(channel, reply)



if __name__ == "__main__":
    main()
