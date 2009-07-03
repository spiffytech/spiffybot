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


def echo(connection, event, args=None):
    '''If two people say the same thing immediately after each other, echo them'''
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    lastMessages = cursor.execute("select * from messages where channel=? order by time desc limit 3", (event.target(),)).fetchall()
    if lastMessages[0][2] == lastMessages[1][2] and lastMessages[0][2] != lastMessages[2][2]: # echo once
        if re.search("^[^!.]", lastMessages[0][2]): # don't echo common IRC commands starting with ! or .
            if lastMessages[0][0] != lastMessages[1][0]: # different nicks
                connection.privmsg(event.target(), lastMessages[0][2])
