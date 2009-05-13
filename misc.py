# Miscelaneous commands that don't really fit anywhere else

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
