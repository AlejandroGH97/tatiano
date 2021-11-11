from sqlite3 import connect
from math import log10, sqrt, ceil

DB_PATH = "./data/db/database.db"

def connectDB():
    return connect(DB_PATH, check_same_thread=False)

def checkUser(user_id):
    cxn = connectDB()
    cursor = cxn.execute(f'''SELECT COUNT(USER_ID) FROM HUNTERS WHERE USER_ID = {user_id}''')
    exists = cursor.fetchone()[0]
    if exists == 0:
        cxn.execute(f'''INSERT INTO HUNTERS (USER_ID, LAST_HUNT, MONEY) VALUES ({user_id}, julianday("now") - 1, 0)''')
        cxn.commit()
    cxn.close()


def userCanHunt(user_id):
    cxn = connectDB()
    cursor = cxn.execute(f'''SELECT ABS(JULIANDAY(LAST_HUNT) - JULIANDAY("now")) FROM HUNTERS WHERE USER_ID = {user_id}''')
    lastHunt = cursor.fetchone()[0] * 24 * 60
    cxn.close()
    return lastHunt > 15, ceil(15-lastHunt)

def getSpecies():
    cxn = connectDB()
    cursor = cxn.execute(f'''SELECT * FROM SPECIES''')
    species = cursor.fetchall()
    cxn.close()
    return species

def catch(user_id, species_id):
    cxn = connectDB()
    res = cxn.execute(f'''SELECT ID, QUANTITY FROM INVENTORY WHERE USER_ID = {user_id} AND SPECIES_ID = {species_id}''').fetchall()
    print(res)
    if len(res) < 1:
        cxn.execute(f'''INSERT INTO INVENTORY (USER_ID, SPECIES_ID, QUANTITY) VALUES ({user_id}, {species_id}, 1)''')
    else:
        row = res[0]
        print('id',row[0],'newcount',row[1]+1)
        cxn.execute(f'''UPDATE INVENTORY SET QUANTITY = {row[1]+1} WHERE ID = {row[0]}''')
    cxn.commit()
    cxn.close()

def userHunted(user_id):
    cxn = connectDB()
    cxn.execute(f'''UPDATE HUNTERS SET LAST_HUNT = JULIANDAY("now") WHERE USER_ID = {user_id}''')
    cxn.commit()
    cxn.close()

def getInventory(user_id):
    cxn = connectDB()
    cursor = cxn.execute(f'''SELECT SPECIES.NAME, INVENTORY.QUANTITY FROM INVENTORY JOIN SPECIES ON INVENTORY.SPECIES_ID = SPECIES.ID WHERE USER_ID = {user_id}''')
    inventory = cursor.fetchall()
    cxn.close()
    return inventory

def getMoney(user_id):
    cxn = connectDB()
    money = cxn.execute(f'''SELECT MONEY FROM HUNTERS WHERE USER_ID = {user_id}''').fetchone()[0]
    cxn.close()
    return money

def checkValidSale(user_id, specie, quantity):
    cxn = connectDB()
    species = cxn.execute(f'''SELECT ID,RARITY FROM SPECIES WHERE NAME = "{specie}"''').fetchone()
    if species == None:
        return False, -1, 0
    userQuantity = cxn.execute(f'''SELECT QUANTITY FROM INVENTORY WHERE USER_ID = {user_id} AND SPECIES_ID = {species[0]}''').fetchone()[0]
    return userQuantity >= quantity, species[0], species[1]

def sell(user_id, rarity, quantity, specie_id):
    cxn = connectDB()
    multiplier = 1 + (log10(quantity) / (rarity * ((1 + sqrt(5)) / 2)))
    base = 50 / (0.05 * rarity ** 3)
    total = round(quantity * base * multiplier,2)
    cxn.execute(f'''UPDATE INVENTORY SET QUANTITY = QUANTITY - {quantity} WHERE USER_ID = {user_id} AND SPECIES_ID = {specie_id}''')
    cxn.execute(f'''UPDATE HUNTERS SET MONEY = MONEY + {total} WHERE USER_ID = {user_id}''')
    cxn.commit()
    cxn.close()
    return total

def getLeaderboard():
    cxn = connectDB()
    result = cxn.execute('''SELECT USER_ID, MONEY FROM HUNTERS ORDER BY MONEY DESC LIMIT 10''').fetchall()
    cxn.close()
    return result

def getRates():
    cxn = connectDB()
    speciesRates = cxn.execute('''SELECT NAME, RARITY FROM SPECIES ORDER BY RARITY ASC''').fetchall()
    cxn.close()
    return speciesRates

