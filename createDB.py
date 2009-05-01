from sqlite3 import dbapi2 as sqlite

def createDB(dbName):
    dbConn = sqlite.connect(dbName)
    cursor = dbConn.cursor()

    cursor.execute('''CREATE TABLE "connEvents" (
    "user" TEXT,
    "event" TEXT,
    "channel" TEXT,
    "time" TEXT
)''')

    cursor.execute('''CREATE TABLE "messages" (
    "user" TEXT,
    "channel" TEXT,
    "message" TEXT,
    "time" TEXT
)''')

    cursor.execute('''CREATE TABLE topic_history (
    "topic" TEXT,
    "time" TEXT,
    "user" TEXT
, "channel" TEXT)''')

    cursor.execute('''CREATE TABLE "trivia" (
    "submitter" TEXT,
    "text" TEXT
)''')

    dbConn.commit()
    dbConn.close()
