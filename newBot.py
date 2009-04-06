#!/usr/bin/env python

import irclib
import commands

# Connection information
network = 'irc.freenode.net'
port = 6667
channel = '#bottest'
nick = 'spiffybot'
realName = 'spiffybot'


def main():

    # Create an IRC object
    irc = irclib.IRC()
#    irclib.DEBUG = True

    # Create a server object, connect and join the channel
    server = irc.server()
    server.connect(network, port, nick, ircname = realName)
    server.join(channel)
    server.privmsg(channel, "Feed me.")

    # Add event handlers
    irc.add_global_handler("pubmsg", gotMessage)
    irc.add_global_handler("privmsg", gotMessage)
    irc.add_global_handler("join", handleJoin)
    irc.add_global_handler("part", handleJoin)
    irc.add_global_handler("kick", handleJoin)
    irc.add_global_handler("invite", handleInvite)


    # Jump into an infinite loop
    irc.process_forever()



def handleJoin(connection, event):
    pass

def handlePart(connection, event):
    pass

def handleKick(connection, event):
    pass

def handleInvite(connection, event):
    connection.join(event.arguments()[0])


def gotMessage(connection, event):
    '''Someone sent a message to a channel!'''
    sender = event.source().split("!")[0]  # Who sent the message
    message = event.arguments()[0].split()  # Get the channel's new message and split it for parsing
    if message[0].startswith(nick):  # If it's a command for us:
        command = message[1]
        args = " ".join(message[2:])  # Quite unexplainably, this will never throw an index-out-of-range error

        # Run the specified command
        if command == "update":
            updateCommands()  # Update the command list
        try:  # See if we have a command in our list to match what the user told us to do; if so, do it.
            commands.cmds[command](connection, event, args)
        except KeyError:  # OK, so we don't have a simple command. Look for a more advanced (e.g.,"natural language") command
            reply = "Maybe."  # Respond with this if we don't have anything else to respond with
            connection.privmsg(channel, reply)



def updateCommands():
    '''Reload the main commands file'''
    reload(commands)



if __name__ == "__main__":
    main()
