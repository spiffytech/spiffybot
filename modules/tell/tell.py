#!/usr/bin/env python
# Brian Cottingham
# spiffytech@gmail.com
# 2009-05-07
# Delivers messages to users either at a specified time, or when they next join/talk

# This file is part of Spiffybot.
# 
# Spiffybot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Spiffybot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Spiffybot.  If not, see <http://www.gnu.org/licenses/>.


from sqlite3 import dbapi2 as sqlite

import epochTools
import os
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import time


dbName = "logs.db"

def tell(event):
    '''Saves a message to deliver to someone later'''
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    try:
        sendee = event.args.split()[0].lower()  # To whom should the message be delivered
    except:
        event.reply("You didn't send me a valid argument!")
        return
    if sendee == "me" or sendee == "myself":
        sendee = event.sender
    message = " ".join(event.args.split()[1:])
    if len(message.split(" in ")) > 1:
        message = " ".join(message.split(" in ")[:-1])

    # Parse the time to deliver the message (if any)
    deliver = event.args.split(" in ")[-1]
    p = pdt.Calendar(pdc.Constants())  # Use parsedatetime module to easily handle human date formatting
    deliver = p.parse(deliver)
    if deliver[1] == 0:  # Tried to parse an invalid time (i.e., we can't parse "stuff")
        deliver = None
    else:
        deliver = deliver[0]
        deliver = "%d-%d-%d %d:%d:%d" % (deliver[0], deliver[1], deliver[2], deliver[3], deliver[4], deliver[5])  # Format the deliver into a string for toEpoch()
        deliver = epochTools.toEpoch(deliver, format="%Y-%m-%d %H:%M:%S")  # deliverstamp for DB storage

    cursor.execute("insert into tell (sender, sendee, channel, message, deliver, sent) values (?, ?, ?, ?, ?, ?)", (event.sender, sendee, event.channel, message, deliver, time.time()))
    event.reply("Will do!")
    dbConn.commit()



def deliverMessages(event=None):  # Use None for the timed message delivery, which passes no events
    '''Checks to see if there's a message to deliver'''
    # TODO: cross-channel notification
    # Global notification
    # Specify a channel to notify in
    # Set notification by PM
    # Make sure a user is in the channel before delivering a timed message
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    # Deliver messages based on user events (join, pubmsg)
    if event == None or (event.eventType == "pubmsg" or "join"):  # See if someone came back from idle or joined
        messages = cursor.execute("select sender, sendee, message, channel, sent from tell where sendee=? and channel=?", (event.sender, event.channel)).fetchall()
        cursor.execute("delete from tell where sendee=? and channel=?", (event.sender, event.channel))
    # Deliver messages that were marked for delivery at a specific time
    else:
        currentTime = time.time()  # Save the current time to account for seconds change between next two lines
#        print currentTime
#        print cursor.execute("select deliver from tell where sendee='dood2'").fetchall()
        messages = cursor.execute("select event.sender, sendee, message, event.channel, sent from tell where deliver<=?", (currentTime,)).fetchall()
        cursor.execute("delete from tell where deliver<=?", (currentTime,))

    # Send the messages resultant from the above DB queries
    for message in messages:
        sender = message[0]
        sendee = message[1]
        messageText = message[2]
        channel = message[3]
        deliveryTime = epochTools.fromEpoch(message[4])
        event.reply("%s, message from %s at %s: %s" % (sendee, sender, deliveryTime, messageText))
    dbConn.commit()
