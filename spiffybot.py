#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Brian Cottingham
# spiffyech@gmail.com
# 2009-05-12
# A fairly simple, yet capable, IRC bot

import os
import random
import re
import readline
from sqlite3 import dbapi2 as sqlite
import string
import sys
import time
import traceback

import commands
from createDB import createDB
import irclib
import ircTools
import misc
import tell

# ==========
# Temporary imports until automatic plugin infrastructure is in place
from calc import calc
import help
from ircTools import ircTools
from mcode import mcode
from tell import tell
from misc import misc
from roulette import roulette
from stocks import stocks
from tiny import tiny
from weather import weather
from woot import wootoff
# =========



if len(sys.argv) > 1 and sys.argv[1] == "--debug":
    DEBUG = True
else:
    DEBUG = False


def printException(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    print excName
    print excArgs
    print "\n".join(excTb)

# Open the database
dbName = "logs.db"
if not os.path.exists(dbName):
    createDB(dbName)
    os.popen("./importTrivia.py").read()
dbConn = sqlite.connect(dbName)
cursor = dbConn.cursor()


# IRC connection information
network = 'irc.freenode.net'
port = 6667
channels = ['##bottest',]
nick = 'spiffybot'
realName = 'spiffybot'


def main():
    # Create an IRC object
    irc = irclib.IRC()
    if DEBUG:
        irclib.DEBUG = True  # Uncomment this to dump all irclib events to stdout

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
    while 1:
        if not DEBUG:
            try:
                irc.process_forever()
            except KeyboardInterrupt:
                break
            except:
                server.privmsg("spiffytech", "I crashed!")
        else:
            irc.process_forever()
            print "here"


def changeNick(connection=None, event=None, newNick=None):
    '''If the bot's nick is used, this function generates another nick'''
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
    '''Log channel all connection events to the database. There's no real reason for it presently; just doing it for kicks and giggles.'''
    global dbConn
    global cursor
    user = event.sourceuser().decode("utf-8")
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
    alterer = event.sourceuser().decode("utf-8")  # Who changed the topic
    topic = event.arguments()[0].decode("utf-8")  # New topic
    alteredTime = str(time.time())
    cursor.execute("insert into topic_history values (?, ?, ?, ?)", (topic, alteredTime, alterer, event.target()))
    dbConn.commit()


def handleMessage(connection, event):
    '''Someone sent a message to a channel!'''

    # Parse the raw IRC data contents
    sender = event.sourceuser().decode("utf-8")  # Who sent the message
    message = event.arguments()[0].decode("utf-8")  # Get the channel's new message and split it for parsing

    # BEFORE ANYTHING ELSE, record the message in our logs
    global dbConn
    global cursor
    cursor.execute("insert into messages values (?, ?, ?, ?)", (sender, event.target(), message, unicode(time.time())))
    dbConn.commit()

    # First, see if this triggers a message delivery for someone
    tell.deliverMessages(connection, event)
    # Next, check for echoes
    ircTools.echo(connection, event)

    # Next, see if the message is something we care about (i.e., a command)
    if message[0:len(nick)].lower() == nick.lower() or event.eventtype() == "privmsg":  # If it's a command for us:
        # ^^ startswith: "spiffybot: calc" || privmsg part ensures this code is triggered if the message is a PM
        if not event.eventtype() == "privmsg":
            message = message.partition(" ")[2]  # No nick at the front of a private message

        # Run the specified command

        for command in commands.cmds:
            r = re.search(command[0], message)
            if r != None:
                args = message[r.end():].strip()  # For now, a command always starts the message. args is whatever comes after the command.
                execString = command[1] + "(connection, event, args)"  # Using a string instead of storing the function facilitates the planned automatic module loading feature.
                eval(execString)
                return

        reply = "Maybe."  # Respond with this if we don't have anything else to respond with
        connection.privmsg(event.target(), reply)



def cmdJoin(connection, event, args):
    connection.join(args)
def cmdNick(connection, event, args):
            connection.nick(args)
            global nick
            nick = args
def cmdPart(connection, event, args):
    connection.part(event.target())


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
        time.sleep(3)
        tell.deliverMessages(conn)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting..."
