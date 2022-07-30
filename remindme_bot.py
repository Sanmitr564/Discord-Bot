import datetime
import sched
from time import sleep, time
from tokenize import Token
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv

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

# !pingme at time, message
# !pingme every time, message
# !pingme in time, message

def initialize_time():
    now = datetime.datetime.now()
    begin = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute= now.minute + 1)
    delta = begin-now
    s = sched.scheduler(time, sleep)
    s.enter(delta.total_seconds(), 0, begin_time)
    s.run()

def begin_time():
    check_reminders.start()

@tasks.loop(minutes=1)
async def check_reminders():
    pass

@bot.command(aliases = ['at'])
async def _notif_at(ctx: commands.Context, *, args):
    notif = input_at_time(args)
    if notif:
        reminders.append(notif)
        await ctx.send(notif)

@bot.event
async def on_ready():
    print('Bot is online!')
    initialize_time()
    

bot.run(TOKEN)