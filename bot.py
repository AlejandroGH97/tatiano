import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import hunting
import db


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')

intents = discord.Intents().all()
client = commands.Bot(command_prefix = PREFIX, intents=intents)
client.remove_command('help')
@client.event
async def on_ready():
    print('Ready.')

@client.command(aliases=["Hunt", "HUNT"])
async def hunt(context):
    db.checkUser(context.message.author.id)
    response = hunting.hunt(context.message.author)
    await context.send(embed=response)

@client.command(aliases=["inv", "Inv", "INV", "Inventory", "INVENTORY"])
async def inventory(context):
    inventory = hunting.getInventory(context.message.author)
    await context.send(embed=inventory)

@client.command(aliases=["Money", "MONEY", "cash", "Cash", "CASH"])
async def money(context):
    response = hunting.getMoney(context.message.author)
    await context.send(embed=response)

@client.command(aliases=["Sell", "SELL"])
async def sell(context):
    user = context.message.author
    params = context.message.content[2:].split()
    specie = ' '.join(w.capitalize() for w in params[1:-1])
    quantity = int(params[-1])
    if params[-1].isdigit():
        response = hunting.sell(user, specie, quantity)
    else:
        response = discord.Embed(
            description=f"Invalid request, correct usage is ~!sell **specie_name quantity**.",
            color=0xFFFF00
        )
    await context.send(embed=response)

@client.command(aliases=["Help", "HELP", "h", "H"])
async def help(context):
    response = discord.Embed(
            description=f"This is what Tatiano is able to do.",
            color=0xFFFF00
        )
    commandValues = "Hunt\nInventory[inv]\nMoney\nSell specie_name quantity"
    descValues = "Go out hunting (15 min CD).\nCheck your inventory.\nCheck your current balance.\nSells species from your inventory."
    response.add_field(
        name="Hunting:",
        value='Commands for all hunting related activities.',
        inline=False
        )
    response.add_field(
        name="Commands:",
        value=commandValues,
        inline=True
        )
    response.add_field(
        name="Description:",
        value=descValues,
        inline=True
    )
    await context.send(embed=response)

@client.command(aliases=["Leaderboard", "LEADERBOARD"])
async def leaderboard(context):
    await context.send(embed=hunting.leaderboard())

@client.command(aliases=["Rates", "RATES"])
async def rates(context):
    await context.send(embed=hunting.huntRates())

@client.command(aliases=["Check", "CHECK"])
async def check(context):
    params = context.message.content[2:].split()
    specie = ' '.join(w.capitalize() for w in params[1:-1])
    quantity = int(params[-1])
    response = hunting.checkPrice(specie, quantity)
    await context.send(embed=response)



client.run(TOKEN)


"""
TODO
-Check price
-Trade species
"""