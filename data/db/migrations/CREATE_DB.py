from sqlite3 import connect

DB_PATH = "../database.db"
cxn = connect(DB_PATH)
cxn.close()