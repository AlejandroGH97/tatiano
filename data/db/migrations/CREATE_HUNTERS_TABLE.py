from sqlite3 import connect

DB_PATH = "../database.db"
cxn = connect(DB_PATH)
cxn.execute('''CREATE TABLE HUNTERS
        (USER_ID TEXT PRIMARY KEY NOT NULL,
        LAST_HUNT DATETIME,
        MONEY REAL DEFAULT 0);''')
cxn.close()