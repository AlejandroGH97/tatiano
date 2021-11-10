from sqlite3 import connect

DB_PATH = "../database.db"
cxn = connect(DB_PATH)

species = [
    {'name' : 'Seahorse', 'source': 'https://c.tenor.com/Pv2ID_eZxaAAAAAC/seahorse-pixel.gif', 'rarity': 0.75},
    {'name': 'Redfish', 'source': 'https://c.tenor.com/sIXN0BuHwAkAAAAC/pixel-art.gif', 'rarity': 1},
    {'name': 'Pelicanus', 'source': 'https://c.tenor.com/O_TJ39doD64AAAAS/fish-big.gif', 'rarity': 0.8},
    {'name': 'Deep Sea Anglerfish', 'source': 'https://c.tenor.com/ycJ522k8-CYAAAAC/monster-fish.gif', 'rarity': 0.7},
    {'name': 'Orchid Dottyback', 'source': 'https://c.tenor.com/w1EWXDpMSsgAAAAC/fish-blue.gif', 'rarity': 0.9},
    {'name': 'Eel', 'source': 'https://c.tenor.com/TwyDLatwPDQAAAAC/fish-blue.gif', 'rarity': 1.5},
    {'name': 'Mutant Fly', 'source': 'https://c.tenor.com/t9Yrsnwu3xwAAAAC/florida-monster.gif', 'rarity': 1.5},
    {'name': 'Sprite', 'source': 'https://c.tenor.com/FeWWoJ0mvxMAAAAd/fate-monster.gif', 'rarity': 0.05},
    {'name': 'Grand Magus', 'source': 'https://c.tenor.com/NqkA3iRcqREAAAAC/pixel-art.gif', 'rarity': 0.01},
    {'name': 'Bean Demon', 'source': 'https://c.tenor.com/gFvc0poigIYAAAAC/demon-red.gif', 'rarity': 0.1},
    {'name': 'Toxic Shroom', 'source': 'https://c.tenor.com/0RvKuBLj300AAAAC/mushroom-purple.gif', 'rarity': 0.2},
    {'name': 'Hog', 'source': 'https://c.tenor.com/xqfEXcIDhXEAAAAS/javali-monster.gif', 'rarity': 0.6}
]

for specimen in species:
    cxn.execute(f'''INSERT INTO SPECIES (NAME, RARITY, SOURCE) VALUES (\"{specimen["name"]}\", {specimen["rarity"]}, \"{specimen["source"]}\")''')

cxn.commit()
cxn.close()