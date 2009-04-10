#!/usr/bin/env python
# Brian Cottingham
# spiffyech@gmail.com
# 2009-04-09
# A fairly simple, yet capable, IRC bot

import irclib
import commands
import os
from sqlite3 import dbapi2 as sqlite
import time

# Initialize the logs database
dbName = "logs.db"
if not os.path.exists(dbName):
    print "Creating new database..."
    conn = sqlite.connect(dbName)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE todos (id INTEGER PRIMARY KEY, completed VARCHAR(5), duedate VARCHAR(30), priority INTEGER, title VARCHAR(150), description VARCHAR(3000))")
    cursor.execute("create table idmap (id INTEGER, realid INTEGER)")
    conn.close()

dbConn = sqlite.connect(dbName)
cursor = dbConn.cursor()

# IRC connection information
network = 'irc.freenode.net'
port = 6667
channels = ['#bottest',]
nick = 'spiffybot'
realName = 'spiffybot'


def main():
    # Create an IRC object
    irc = irclib.IRC()
#    irclib.DEBUG = True  # Uncomment this to dump all irclib events to stdout

    # Create a server object, connect and join the channels
    server = irc.server()
    server.connect(network, port, nick, ircname = realName)
    for channel in channels:
        server.join(channel)
    server.privmsg(channel, "Feed me.")  # Send message to channel when we join it

    # Add handler functions for various IRC events
    irc.add_global_handler("pubmsg", handleMessage)
    irc.add_global_handler("privmsg", handleMessage)
    irc.add_global_handler("join", handleJoin)
    irc.add_global_handler("part", handlePart)
    irc.add_global_handler("quit", handleQuit)
    irc.add_global_handler("kick", handleKick)
    irc.add_global_handler("topic", handleTopic)


    # Fork off our child process for controller input
    pid = os.fork()
    if pid:
        child_process(server)

    # In the parent process, start monitoring the channel
    irc.process_forever()


########## Functions to handle channel user connection events ##########
def handleJoin(connection, event):
    recordEvent(connection, event)

def handlePart(connection, event):
    recordEvent(connection, event)

def handleQuit(connection, event):
    recordEvent(connection, event)

def handleKick(connection, event):
    recordEvent(connection, event)

def recordEvent(connection, event):
    global dbConn
    global cursor
    user = event.source().split('!')[0]
    alteredTime = str(time.time())
    channel = event.target()
    cursor.execute("insert into connevents values ('%s', '%s', '%s', '%s')" % (user, event.eventtype(), channel, alteredTime))
    dbConn.commit()
########################################################################


def handleTopic(connection, event):
    global dbConn
    global cursor
    alterer = event.source().split('!')[0]
    topic = event.arguments()[0]
    alteredTime = str(time.time())
    cursor.execute("insert into topic_history values ('%s', '%s', '%s', '%s')" % (topic, alteredTime, alterer, event.target()))
    dbConn.commit()


def handleMessage(connection, event):
    '''Someone sent a message to a channel!'''
    sender = event.source().split("!")[0]  # Who sent the message
    message = event.arguments()[0].split()  # Get the channel's new message and split it for parsing

    if (message[0].startswith(nick) or not event.target().startswith("#")) and len(message) > 1:  # If it's a command for us:
        if not message[0].startswith(nick):  # No bot nick passed by a private message command
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
            connection.privmsg(event.target(), reply)



def updateCommands():
    '''Reload the main commands file'''
    reload(commands)



def child_process(conn):
    '''Child process main function- reads input from the user and sends it to the channels'''
    if not "channel" in locals():
        channel = channels[0]
    while 1:
        msg = raw_input("Talk to channel: ")
        if msg.startswith("="):  # Set the channel we want to talk to
            # Examples: "=#ncsulug", "=#ncsulug Send this message!"
            msg = msg.split()
            channel = msg[0].split("=")[1]
            if len(msg) > 1:
                conn.privmsg(channel, " ".join(msg[1:]))
            continue
        conn.privmsg(channel, msg)



if __name__ == "__main__":
    main()
