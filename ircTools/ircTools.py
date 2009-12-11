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

def topics(event):
    '''Lists the previous $args topics set in a channel'''
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    if not re.match("^\d$", event.args):  # Check whether we were given a count of topics to present
        event.args = str(3)
    elif int(event.args) > 10:
        event.args = (10)
        

    topics = cursor.execute("select * from topic_history where channel=? order by time desc limit ?;", (event.channel, event.args) )
    topics = topics.fetchall()[::-1]

    if len(topics) == 0:
        event.reply("No topics in history")
    else:
        for topic in topics: 
            alteredTime = fromEpoch(topic[1], secs=1)  # Altered time is stored in the DB in epoch format. Convert out of that.
            event.reply("Set on %s by %s: %s" % (alteredTime, topic[2], topic[0]))  #Send to the channel


def echo(event):
    '''If two people say the same thing immediately after each other, echo them'''

#    if event.eventType == "privmsg":
#        return

    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    lastMessages = cursor.execute("select * from messages where channel=? order by time desc limit 3", (event.channel,)).fetchall()
    if len(lastMessages) < 2:  # First message in this channel, no echo possible
        return
    if lastMessages[0][2] == lastMessages[1][2] and lastMessages[0][2] != lastMessages[2][2]:  # Don't echo a message if you've already done so
        print "\n\neverywhere\n"
        if re.search("^[^!.]", lastMessages[0][2]): # don't echo common IRC commands starting with ! or .
            print "\n\nnowhere\n"
            if lastMessages[0][0] != lastMessages[1][0]:  # Only echo if different users are talking
                print "\n\nthere\n"
                event.reply(lastMessages[0][2])
