# Brian Cottingham
# 2009-04-14
# Imports trivia from a file into the database
# Nothing special, just a timesaver. 

from sqlite3 import dbapi2 as sqlite

dbConn = sqlite.connect("logs.db")
cursor = dbConn.cursor()

inFile = open("trivia.txt", 'r')
facts = inFile.readlines()
inFile.close()

for fact in facts:
    if fact == "\n":
        continue
    cursor.execute("insert into trivia values (?, 'spiffytech')", (fact,))

dbConn.commit()
