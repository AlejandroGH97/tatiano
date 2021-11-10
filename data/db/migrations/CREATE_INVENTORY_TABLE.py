from sqlite3 import connect

DB_PATH = "../database.db"
cxn = connect(DB_PATH)
cxn.execute('''CREATE TABLE INVENTORY
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID TEXT,
        SPECIES_ID INT,
        QUANTITY INT DEFAULT 0,
        FOREIGN KEY (USER_ID) REFERENCES HUNTERS (USER_ID),
        FOREIGN KEY (SPECIES_ID) REFERENCES SPECIES (ID));''')
cxn.close()