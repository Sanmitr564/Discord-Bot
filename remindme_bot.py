import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")

bot = commands.Bot(command_prefix='pm! ')
reminders = []

@bot.command
async def pingMe(ctx: commands.Context):
    
