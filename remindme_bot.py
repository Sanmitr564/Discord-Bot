import datetime
from tokenize import Token
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
TOKEN = getenv('TOKEN')

bot = commands.Bot(command_prefix='!pingme ')
reminders = []

@bot.command
async def pingMe(ctx: commands.Context):
    pass

@bot.event
async def on_ready():
    print('Bot is online!')

bot.run(TOKEN)
