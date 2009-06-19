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

def createDB(dbName):
    # The workings of this function should be pretty obvious
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    # This table is for logging joins/parts/kicks
    cursor.execute('''CREATE TABLE "connEvents" (
    "user" TEXT,
    "event" TEXT,
    "channel" TEXT,
    "time" TEXT
    )''')

    # This table is for regular messages
    cursor.execute('''CREATE TABLE "messages" (
    "user" TEXT,
    "channel" TEXT,
    "message" TEXT,
    "time" TEXT
    )''')

    # This table is for logging topics for each channel
    cursor.execute('''CREATE TABLE topic_history (
    "topic" TEXT,
    "time" TEXT,
    "user" TEXT
    , "channel" TEXT)''')

    # This table is for storing random facts for the trivial function
    cursor.execute('''CREATE TABLE "trivia" (
    "submitter" TEXT,
    "text" TEXT
    )''')

    # This table stores temporally asynchronous messages between users
    cursor.execute('''CREATE TABLE tell (
        "sender" TEXT,
        "sendee" TEXT,
        "message" TEXT,
        "deliver" TEXT,
        "sent" TEXT
    , "channel" TEXT
    )''')


    dbConn.commit()
    dbConn.close()
