#!/usr/bin/env python
# Brian Cottingham
# spiffytech@gmail.com
# 2009-05-07
# Delivers messages to users either at a specified time, or when they next join/talk


from sqlite3 import dbapi2 as sqlite

import epochTools
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import time


dbName = "logs.db"

def tell(connection, event, args):
    '''Saves a message to deliver to someone later'''
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    sender = event.source().split("!")[0]
    sendee = args.split()[0].lower()  # To whom should the message be delivered
    if sendee == "me" or sendee == "myself":
        sendee = sender
    print sendee
    channel = event.target()
    message = " ".join(args.split()[1:])
    if len(message.split(" in ")) > 1:
        message = " ".join(message.split(" in ")[:-1])

    # Parse the time to deliver the message (if any)
    deliver = args.split(" in ")[-1]
    p = pdt.Calendar(pdc.Constants())  # Use parsedatetime module to easily handle human date formatting
    deliver = p.parse(deliver)
    if deliver[1] == 0:  # Tried to parse an invalid time (i.e., we can't parse "stuff")
        deliver = None
    else:
        deliver = deliver[0]
        deliver = "%d-%d-%d %d:%d:%d" % (deliver[0], deliver[1], deliver[2], deliver[3], deliver[4], deliver[5])  # Format the deliver into a string for toEpoch()
        deliver = epochTools.toEpoch(deliver, format="%Y-%m-%d %H:%M:%S")  # deliverstamp for DB storage

    cursor.execute("insert into tell (sender, sendee, channel, message, deliver, sent) values (?, ?, ?, ?, ?, ?)", (sender, sendee, channel, message, deliver, time.time()))
    connection.privmsg(event.target(), "Will do!")
    dbConn.commit()



def deliverMessages(connection=None, event=None, args=None): 
    '''Checks to see if there's a message to deliver'''
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    if event != None and (event.eventtype() == "pubmsg" or event.eventtype() == "join"):  # See if someone came back from idle or joined
        sender = event.source().split("!")[0].lower()
        messages = cursor.execute("select sender, sendee, message, channel, sent from tell where sendee=?", (sender,)).fetchall()
        cursor.execute("delete from tell where sendee=?", (sender,))
    else:
        currentTime = time.time()  # Save time to account for seconds change between next two lines
        messages = cursor.execute("select sender, sendee, message, channel, sent from tell where deliver<=?", (currentTime,)).fetchall()
        cursor.execute("delete from tell where deliver<=?", (currentTime,))

    for message in messages:
        sender = message[0]
        sendee = message[1]
        messageText = message[2]
        channel = message[3]
        deliveryTime = epochTools.fromEpoch(message[4])
        connection.privmsg(channel, "%s, message from %s at %s: %s" % (sendee, sender, deliveryTime, messageText))
    dbConn.commit()
