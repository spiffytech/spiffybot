from sqlite3 import dbapi2 as sqlite
from epochTools import *
import re

dbName = "logs.db"

def topics(connection, event, args):
    '''Lists the previous $args topics set in a channel'''
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    if not re.match("\d", args):  # Oh, goodie- input validation
        args = 3

    topics = cursor.execute("select * from topic_history where channel=? order by time;", (event.target(),) )
    topics = topics.fetchall()[:int(args)]

    if len(topics) == 0:
        connection.privmsg(event.target(), "No topics in history")
    else:
        for topic in topics: 
            alteredTime = fromEpoch(topic[1], secs=1)  # Altered time is stored in the DB in epoch format. Convert out of that.
            connection.privmsg(event.target(), "On %s by %s: %s" % (alteredTime, topic[2], topic[0]))  #Send to the channel
