from sqlite3 import connect

DB_PATH = "../database.db"
cxn = connect(DB_PATH)
cxn.execute('''CREATE TABLE SPECIES
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        RARITY REAL NOT NULL,
        SOURCE TEXT NOT NULL);''')
cxn.close()