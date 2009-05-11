#!/usr/bin/env python
# Brian Cottingham
# spiffyech@gmail.com
# 2009-05-11
# A fairly simple, yet capable, IRC bot

import os
import random
import readline
from sqlite3 import dbapi2 as sqlite
import string
import time

import irclib
import commands
from createDB import createDB
import tell


# Open the database
dbName = "logs.db"
if not os.path.exists(dbName):
    createDB(dbName)
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
    global server
    server = irc.server()
    server.connect(network, port, nick, ircname = realName)
    joinChannels()


    # Add handler functions for various IRC events
    irc.add_global_handler("pubmsg", handleMessage)
    irc.add_global_handler("privmsg", handleMessage)
    irc.add_global_handler("join", handleJoin)
    irc.add_global_handler("part", handlePart)
    irc.add_global_handler("quit", handleQuit)
    irc.add_global_handler("kick", handleKick)
    irc.add_global_handler("topic", handleTopic)
    irc.add_global_handler("nicknameinuse", changeNick)


    # Fork off our child process for operator input
    pid = os.fork()
    if pid:
        termInput(server)
    pid = os.fork()
    if pid:
        watchLoop(server)

    # In the parent process, start monitoring the channel
    irc.process_forever()


def changeNick(connection=None, event=None, newNick=None):
    if connection == None and event == None:  # Called within newBot.py, not from an event handler
        connection.nick(newNick)
        nick = newNick

    else:
        newNick = ""
        if len(connection.nickname) < 15:
            connection.nick(connection.nickname +  "_")
            joinChannels(connection)
        else:
            chars = string.letters + string.numbers
            random.seed(time.time)
            for i in range(0, random.randint(2, len(string.digits)-1)):
                newNick += chars[random.randint(0, len("".letters)-1)]
            connection.nick(newNick)
            joinChannels(connection)


########## Functions to handle channel user connection events ##########
# All of these functions just call recordEvent, but are here in case I ever want do do more than that when handling events
def handleJoin(connection, event):
    recordEvent(event)

def handlePart(connection, event):
    recordEvent(event)

def handleQuit(connection, event):
    recordEvent(event)

def handleKick(connection, event):
    recordEvent(event)

def recordEvent(event):
    '''Log all connection events to the database. No real reason, just for kicks and giggles.'''
    global dbConn
    global cursor
    user = event.source().split('!')[0]
    alteredTime = str(time.time())
    channel = event.target()
    type = event.eventtype()
    cursor.execute("insert into connevents values (?, ?, ?, ?)", (user, type, channel, alteredTime))
    dbConn.commit()
########################################################################


def handleTopic(connection, event):
    '''Log topic changes'''
    # TODO: Log topic when first entering a channel
    global dbConn
    global cursor
    alterer = event.source().split('!')[0]  # Who changed the topic
    topic = event.arguments()[0]  # New topic
    alteredTime = str(time.time())
    cursor.execute("insert into topic_history values (?, ?, ?, ?)", (topic, alteredTime, alterer, event.target()))
    dbConn.commit()


def handleMessage(connection, event):
    '''Someone sent a message to a channel!'''

    # First, see if this triggers a message delivery for someone
    tell.deliverMessages(connection, event)

    # Parse the raw IRC data contents
    sender = event.source().split("!")[0]  # Who sent the message
    message = event.arguments()[0].split()  # Get the channel's new message and split it for parsing

    # First, record the message in our logs
    global dbConn
    global cursor
    cursor.execute("insert into messages values (?, ?, ?, ?)", (sender, event.target(), " ".join(message), str(time.time())))
    dbConn.commit()

    # Next, see if the message is something we care about (i.e., a command)
    if (message[0].startswith(nick) or not event.target().startswith("#")) and len(message) > 1:  # If it's a command for us:
        # ^^ startswith: "spiffybot: calc" ; not startswith("#") indicates private message ; len prevents triggers on "spiffybot!"
        # Trim botnick off of front of public messages to make them match private messages, for list index's sake
        if not message[0].startswith(nick):  # No bot nick at start of message indicates a command passed in a private message
            command = message[0]
            args = " ".join(message[1:])
        else:
            command = message[1]
            args = " ".join(message[2:])  # Quite unexplainably, this will never throw an index-out-of-range error

        # Run the specified command
        # Start with a few commands that are best (thanks to coding structure) parsed first
        # TODO: Refactor bot to use internal[] and external[] dicts, rather than this if/elif stuff
        if command == "update":
            updateCommands()  # Update the command list
            return
        elif command == "join":
            connection.join(args)
            return
        elif command == "nick":
            connection.nick(args)
            global nick
            nick = args
            return
        elif (command == "get" and args.split()[0] == "out") or (command == "fail"):
            connection.part(event.target(), message="EPIC CRASH!")  # For unknown reasons, the message sending doesn't work
            return

        try:  # See if we have a command in our list to match what the user told us to do; if so, do it.
            commands.cmds[command](connection, event, args)
        except KeyError:  # OK, so we don't have a simple command. Look for a more advanced (e.g.,"natural language") command
            reply = "Maybe."  # Respond with this if we don't have anything else to respond with
            connection.privmsg(event.target(), reply)



def updateCommands():
    '''Reload the main commands file'''
    # Currently broken
    reload(commands)



def joinChannels(connection=None, event=None):
    # Join all specified channels at program launch
    # In Separate function to facilitate joins after nick collision
    for channel in channels:
        server.join(channel)



def termInput(conn):
    '''Child process that reads input from the user and sends it to the channels'''
    if not "channel" in locals():
        channel = channels[0]
    while 1:
        msg = raw_input("Talk to channel: ")  # Get a message from the user
        if msg.startswith("="):  # Set the channel we want to talk to
            # Examples: "=#ncsulug", "=#ncsulug Send this message!"
            msg = msg.split()
            channel = msg[0].split("=")[1]
            if len(msg) > 1:
                conn.privmsg(channel, " ".join(msg[1:]))
            continue
        conn.privmsg(channel, msg)




def watchLoop(conn):
    while 1:
        tell.deliverMessages(conn)
        time.sleep(5)



if __name__ == "__main__":
    main()
