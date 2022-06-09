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

# 8:30 am 6/7/2022 -> datetime(2022, 6, 7, hour=8, minute=30)
# 
# if it's currently 3 pm,
# 4:20 -> datetime(current year, current month, current day, hour=16, minute=20)
#
# if it's currently 8 pm
# 6 am -> datetime(tomorrows year, tomorrows month, tomorrows day, hour=6, minute=0)
#
# full arguments list () is optional: hour(:minute) (am/pm) (month/day/(year))

def input_at_time(input):
    args = input.split()
    year, month, day, hour, minute = None

    if len(args) > 3:
        return None
    elif len(args) == 3:
        time = args[0]
        ampm = args[1]
        date = args[2]
        
        timestring = time.split(':')
        h, m = 0
        if len(timestring) == 1:
            h = timestring[0]
        elif len(timestring) == 2:
            h = timestring[0]
            m = timestring[1]
        else:
            return None

        if ampm.lower == 'am':
            pass
        elif ampm.lower == 'pm':
            pass
        else:
            return None
        
        


# !pingme at time, message
# !pingme every time, message
# !pingme in time, message

@bot.command(aliases = ['at'])
async def _notif_at(ctx: commands.Context, *, args):
    # notif = input_at_time(args)
    # if notif:
    #     reminders.append(notif)

@bot.event
async def on_ready():
    print('Bot is online!')

bot.run(TOKEN)
