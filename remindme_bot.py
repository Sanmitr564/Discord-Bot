import datetime
from tokenize import Token
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from multiprocessing import Process
from time import sleep

from reminder import Notification

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

def string_to_date(date):
    datestring = None
    if '/' in date:
        datestring = date.split('/')
    elif '-' in date:
        datestring = date.split('-')
    m = d = y = 0;
    if len(datestring) != 3:
        return None
    else:
        m = int(datestring[0])
        d = int(datestring[1])
        y = int(datestring[2]) if int(datestring[2]) > 99 else int(datestring[2]) + 2000
        return m, d, y
    
    
        
def string_to_time(time):
    timestring = time.split(':')
    h = m = 0
    if len(timestring) == 1:
        h = timestring[0]
    elif len(timestring) == 2:
        h = timestring[0]
        m = timestring[1]
    else:
        return None
    return int(h), int(m)

def string_to_ampm(ampm):
    if ampm.lower == 'am':
        return 'am'
    elif ampm.lower == 'pm':
        return 'pm'
    else:
        return None

def input_at_time(input):
    args = input.split()
    year = month = day = hour = minute = None

    if len(args) > 3:
        return None
    elif len(args) == 3:
        hour, minute = string_to_time(args[0])
        ampm = string_to_ampm(args[1])
        month, day, year = string_to_date(args[2])
        notif = datetime.datetime(year, month, day, hour=hour, minute=minute)
        return notif

def per_min():
    while True:
        sleep(1)
        print('second elapsed')

def start():
    bot.run(TOKEN)
# !pingme at time, message
# !pingme every time, message
# !pingme in time, message

@bot.command(aliases = ['at'])
async def _notif_at(ctx: commands.Context, *, args):
    notif = input_at_time(args)
    if notif:
        reminders.append(notif)
        await ctx.send(notif)

@bot.event
async def on_ready():
    print('Bot is online!')

if __name__ == '__main__':
    p1 = Process(target=per_min)
    p2 = Process(target=start)

    p1.start()
    p2.start()
    p1.join()
    p2.join()