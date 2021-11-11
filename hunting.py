import random
import discord
import db

# https://tenor.com/users/mdesk99

def hunt(user):
    canHunt, remaining = db.userCanHunt(user.id)
    if canHunt:
        species = db.getSpecies()
        weights = []
        for specimen in species:
            weights.append(specimen[2])
        catch = random.choices(species, weights=weights, k=1)[0]
        db.catch(user.id,catch[0])
        db.userHunted(user.id)
        response = discord.Embed(
            description=f"{user.mention} has caught a {catch[1]}!",
            color=0xFFFF00,
        )
        response.set_thumbnail(url=catch[3])
        rarity = str(round(catch[2],2))
        response.set_footer(text=f'This specie has a hunt rate of {rarity}!')
        return response
    else:
        response = discord.Embed(
            description=f"Your energy will recover in {remaining} minutes.",
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
    return response

def getMoney(user):
    money = round(db.getMoney(user.id),2)
    response = discord.Embed(
        description=f"{user.mention} has **${money}**.",
        color=0xFFFF00
    )
    return response

def sell(user, specie, quantity):
    validSale, specie_id, rarity = db.checkValidSale(user.id, specie, quantity)
    if quantity > 0 and validSale:
        revenue = db.sell(user.id, rarity, quantity, specie_id)
        response = discord.Embed(
            description=f"{user.mention} sold {quantity} {specie} for **${revenue}**.",
            color=0xFFFF00
        )
        return response
    else:
        if specie_id == -1: # Invalid species name
            response = discord.Embed(
                description=f'Invalid specie name.',
                color=0xFFFF00
            )
        elif quantity < 1:
            response = discord.Embed(
                description=f'Can\'t sell quantities below 1.',
                color=0xFFFF00
            )
        else:
            response = discord.Embed(
                description=f'You do not have enough {specie} to sell.',
                color=0xFFFF00
            )
        return response

def leaderboard():
    leaderboard = db.getLeaderboard()
    user_ids = ''
    money = ''
    for user in leaderboard:
        user_ids += '<@' + user[0] + '>\n'
        money += '$' + str(round(user[1],2)) + '\n'
    response = discord.Embed(
            title="Leaderboard",
            color=0xFFFF00
        )
    response.add_field(
        name='User',
        value=user_ids,
        inline=True
    )
    response.add_field(
        name='Money',
        value=money,
        inline=True
    )
    return response

def huntRates():
    speciesRates = db.getRates()
    species = ''
    rates = ''
    for entry in speciesRates:
        species += entry[0] + '\n'
        rates += str(entry[1]) + '\n'
    response = discord.Embed(
            desc="Hunt rates for all species.",
            color=0xFFFF00
    )
    response.add_field(
        name='Specie',
        value=species,
        inline=True
    )
    response.add_field(
        name='Hunt rate',
        value=rates,
        inline=True
    )
    return response

def checkPrice(specie, quantity):
    rarity = db.getRate(specie)
    if rarity == -1:
        response = discord.Embed(
            description=f'Invalid specie name.',
            color=0xFFFF00
        )
    else:
        price = db.getPrice(rarity, quantity)
        response = discord.Embed(
            description=f'{quantity} {specie} would sell for **${price}**.',
            color=0xFFFF00
        )
    return response