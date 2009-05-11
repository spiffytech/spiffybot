from sqlite3 import dbapi2 as sqlite

import epochTools
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import time

def tell(connection, event, args):
    '''Saves a message to deliver to someone later'''
    dbConn = sqlite.connect("logs.db")
    cursor = dbConn.cursor()

    sender = event.source().split("!")[0]
    sendee = args.split()[0]
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

    cursor.execute("insert into tell (sender, sendee, message, deliver, sent) values (?, ?, ?, ?, ?)", (sender, sendee, message, deliver, time.time()))
    dbConn.commit()
    dbConn.close()
