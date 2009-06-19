# Miscelaneous commands that don't really fit anywhere else

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

dbName = "logs.db"

def trivia(connection, event, args):
    '''Responds with a random trivial fact'''
    dbConn = sqlite.connect("logs.db")
    cursor = dbConn.cursor()

    sender = event.source().split("!")[0]
    fact = cursor.execute("SELECT * FROM trivia ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    connection.privmsg(event.target(), sender+" : "+fact)

def addTrivia(connection, event, args):
    '''Add a trivia fact to the database'''
    dbConn = sqlite.connect("logs.db")
    cursor = dbConn.cursor()

    sender = event.source().split("!")[0]
    cursor.execute("insert into trivia values (?, ?)", (sender, args))
    dbConn.commit()
