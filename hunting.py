import random
import discord
import db


# https://tenor.com/users/mdesk99

def hunt(user):
    if db.userCanHunt(user.id):
        species = db.getSpecies()
        weights = []
        for specimen in species:
            weights.append(specimen[2])
        catch = random.choices(species, weights=weights, k=1)[0]
        db.catch(user.id,catch[0])
        db.userHunted(user.id)
        response = discord.Embed(
            description=f"{user.mention} has caught a {catch[1]}!",
            color=0xFFFF00
        )
        response.set_thumbnail(url=catch[3])
        rarity = "{:.2f}".format(1/catch[2])
        response.set_footer(text=f'This specimen has a rarity of {rarity}!')
        return response
    else:
        response = discord.Embed(
            description=f"You still need to recover energy from your last hunt.",
            color=0xFFFF00
        )
        return response

def getInventory(user):
    inventory = db.getInventory(user.id)
    species = ''
    quantities = ''
    for item in inventory:
        species += item[0] + '\n'
        quantities += str(item[1]) + '\n'
    response = discord.Embed(
            description=f"{user.mention}'s inventory.",
            color=0xFFFF00
        )
    
    response.add_field(name='Species', value=species,  inline=True)
    response.add_field(name='Quantity', value=quantities,  inline=True)
    print(inventory)
    return response

def getMoney(user):
    money = db.getMoney(user.id)
    response = discord.Embed(
            description=f"{user.mention} has **${money}**.",
            color=0xFFFF00
        )
    return response