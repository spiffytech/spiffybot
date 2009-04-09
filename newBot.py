#!/usr/bin/env python

import irclib
import commands
import os

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
    server.privmsg(channel, "Feed me.")  # Send message to channel when we join it

    # Add event handlers
    irc.add_global_handler("pubmsg", gotMessage)
    irc.add_global_handler("privmsg", gotMessage)
    irc.add_global_handler("join", handleJoin)
    irc.add_global_handler("part", handleJoin)
    irc.add_global_handler("kick", handleJoin)


    # Fork off our IRC instance
    pid = os.fork()
    if pid:
        child_process(server)
    irc.process_forever()



def handleJoin(connection, event):
    pass

def handlePart(connection, event):
    pass

def handleKick(connection, event):
    pass


def gotMessage(connection, event):
    '''Someone sent a message to a channel!'''
    sender = event.source().split("!")[0]  # Who sent the message
    message = event.arguments()[0].split()  # Get the channel's new message and split it for parsing
    print "\n" + str(message)
    if message[0].startswith(nick) or not event.target().startswith("#"):  # If it's a command for us:
        if not message[0].startswith(nick):  # No bot nick in a private message command
            command = message[0]
            args = " ".join(message[1:])
        else:
            command = message[1]
            args = " ".join(message[2:])  # Quite unexplainably, this will never throw an index-out-of-range error

        # Run the specified command
        # Start with a few commands that are best (thanks to coding structure) parsed first
        if command == "update":
            updateCommands()  # Update the command list
            return
        elif command == "join":
            connection.join(args)
            return
        elif command == "get" and args.split()[0] == "out":
            print "Leaving channel" + str(event.target())
            connection.part(event.target())
            return

        try:  # See if we have a command in our list to match what the user told us to do; if so, do it.
            commands.cmds[command](connection, event, args)
        except KeyError:  # OK, so we don't have a simple command. Look for a more advanced (e.g.,"natural language") command
            reply = "Maybe."  # Respond with this if we don't have anything else to respond with
            connection.privmsg(channel, reply)



def updateCommands():
    '''Reload the main commands file'''
    reload(commands)



def child_process(conn):
    while 1:
        msg = raw_input("Talk to channel: ")
        conn.privmsg(channel, msg)



if __name__ == "__main__":
    main()
