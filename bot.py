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

@client.event
async def on_ready():
    print('Ready.')

@client.command(aliases=['hunt'])
async def _hunt(context):
    db.checkUser(context.message.author.id)
    response = hunting.hunt(context.message.author)
    await context.send(embed=response)

@client.command(aliases=["inv","inventory"])
async def _inventory(context):
    inventory = hunting.getInventory(context.message.author)
    await context.send(embed=inventory)

@client.command(aliases=["money","cash"])
async def _money(context):
    response = hunting.getMoney(context.message.author)
    await context.send(embed=response)

client.run(TOKEN)


"""
TODO
-Sell from inventory
-Money Leaderboard
-Trade
"""