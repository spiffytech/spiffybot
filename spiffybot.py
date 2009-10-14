#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Brian Cottingham
# spiffyech@gmail.com
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
from misc import misc
#from tell import tell

from modules import *

# Enable debug mode if the appropriate command line parameter was passed
if len(sys.argv) > 1 and sys.argv[1] == "--debug":
    DEBUG = True
else:
    DEBUG = False

# Open the database
dbName = "logs.db"
if not os.path.exists(dbName):
    createDB(dbName)
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
#    irc.add_global_handler("ctcp", handleMessage)  # Commented out until I fix bug that prevents this from logging properly
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

    # In the parent process, start listening for connections
    while 1:
        if not DEBUG:  # Debug CLI arg disables crash message, enables regular Python exception printing, shows irclib raw data
            try:
                irc.process_forever()
            except KeyboardInterrupt:
                break
            except:
                printException()
                server.privmsg("spiffytech", "I crashed!")
        else:
            irc.process_forever()



class ircEvent:
    def __init__(self, connection, event, args):
        self.connection = connection
        self.eventType = event.eventtype()
        self.nick = nick
        self.user = event.sourceuser()  # User who instigated an event (join, part, pubmsg, etc.)
        self.sender = event.source().split("!")[0]
        self.args = args
        if event.target() == self.nick:  # private messages
            self.channel = self.sender
        else:
            self.channel = event.target()
    def reply(self, message):
        self.connection.privmsg(self.channel, message)
    def setNick(self, newNick):
        self.connection.nick(newNick)
        global nick
        nick = newNick



def printException(maxTBlevel=5):
    '''This code is copy/pasted. I don't know how it works, and it doesn't work completely.'''
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


def changeNick(connection=None, event=None, newNick=None):
    '''If the bot's nick is used, this function generates another nick'''
    if connection == None and event == None:  # Called within newBot.py, not from an event handler
        connection.nick(newNick)
        global nick
        nick = newNick
    else:
        newNick = ""
        if len(connection.nickname) < 15:
            newNick = connection.nickname + "_"
            connection.nick(newNick)
            joinChannels(connection)
            nick = newNick
        else:
            chars = string.letters + string.numbers
            random.seed(time.time)
            for i in range(0, random.randint(2, len(string.digits)-1)):
                newNick += chars[random.randint(0, len("".letters)-1)]
            connection.nick(newNick)
            joinChannels(connection)
            nick = newNick


########## Functions to handle channel user connection events ##########
# All of these functions just call recordEvent, but are here in case I ever want do do more than that when handling events
def handleJoin(connection, event):
    event = ircEvent(connection, event, args=None)
    tell.deliverMessages(event)
    recordEvent(event)

def handlePart(connection, event):
    event = ircEvent(connection, event, args=None)
    recordEvent(event)

def handleQuit(connection, event):
    event = ircEvent(connection, event, args=None)
    recordEvent(event)

def handleKick(connection, event):
    event = ircEvent(connection, event, args=None)
    recordEvent(event)

def recordEvent(event):
    '''Log channel all connection events to the database. There's no real reason for it presently; just doing it for kicks and giggles.'''
    global dbConn
    global cursor
    user = event.user.decode("utf-8")
    alteredTime = str(time.time())
    cursor.execute("insert into connevents values (?, ?, ?, ?)", (user, event.eventType, event.channel, alteredTime))
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

    # First, see if this triggers a message delivery for whoever just spoke
    tell.deliverMessages(ircEvent(connection, event, args=None))
    # Next, check for echoes
    ircTools.echo(ircEvent(connection, event, None))

    # See if the message corresponds to any pattern we care about
    for command in commands.anyMessage:
        if DEBUG:
            print command[0]
        r = re.search(command[0], message, re.IGNORECASE)
        if r != None:
            args = r.group("args").strip()
            execString = command[1] + "(ircEvent(connection, event, args))"  # Using a string instead of storing the function facilitates the planned automatic module loading feature.
            eval(execString)


    # Next, see if the message is something we care about (i.e., a command)
    if re.match(nick + "[:\-, ]", message) or event.eventtype() == "privmsg":  # If it's a command for us:
        # ^^ startswith: "spiffybot: calc" || privmsg part ensures this code is triggered if the message is a PM
        if not event.eventtype() == "privmsg":
            message = message.partition(" ")[2]  # No nick at the front of a private message

        # Run the command
        foundMatch = False
        for command in commands.cmds:
            print command[0]
            r = re.search(command[0], message, re.IGNORECASE)
            if r != None:
                foundMatch = True
                args = r.group("args").strip()
                execString = command[1] + "(ircEvent(connection, event, args))"  # Using a string instead of storing the function facilitates the planned automatic module loading feature.
                eval(execString)

        if foundMatch == False:
            connection.privmsg(event.target(), "Maybe")  # Respond with this if we don't have anything else to respond with



def cmdJoin(event):
    event.connection.join(event.args)
def cmdNick(event):
    event.setNick(event.args)
def cmdPart(event):
    event.connection.part(event.channel)


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



def watchLoop(connection):
    while 1:
        time.sleep(3)
#        tell.deliverMessages(ircEvent(connection, event=None, args=None))



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting..."
