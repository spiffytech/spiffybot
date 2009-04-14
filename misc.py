from sqlite3 import dbapi2 as sqlite

dbConn = sqlite.connect("logs.db")
cursor = dbConn.cursor()


def trivia(connection, event, args):
    sender = event.source().split("!")[0]
    fact = cursor.execute("SELECT * FROM trivia ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    connection.privmsg(event.target(), sender+" : "+fact)
