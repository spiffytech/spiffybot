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
