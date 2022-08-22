import datetime
import sched
from asyncio import sleep
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
    m = d = y = 0
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
    if ampm.lower() == 'am':
        return 'am'
    elif ampm.lower() == 'pm':
        return 'pm'
    else:
        return None

def input_at_time(input, ctx: commands.Context):

    message = ""

    if '"' in input:
        if input.find('"') != input.rfind('"'):
            message = input[input.find('"') : input.rfind('"') + 1]
            input = input[input.find('"') - 1 : input.rfind('"') + 1]
    elif "'" in input:
        if input.find("'") != input.rfind("'"):
            message = input[input.find("'"):input.rfind("'")+1]
            input = input[input.find("'") - 1 : input.rfind("'") + 1]
        
    args = input.split()
    

    year = month = day = hour = minute = None

    

    if len(args) > 3:
        return None
    elif len(args) == 3:
        hour, minute = string_to_time(args[0])
        ampm = string_to_ampm(args[1])
        month, day, year = string_to_date(args[2])
        if ampm == 'pm':
            hour += 12
        if not (hour < 24 and minute < 60):
            print('1')
            return None
        if hour is None or minute is None or ampm is None or month is None or day is None or year is None:
            return None
        notif = Notification(
            ctx= ctx,
            time=datetime.datetime(year, month, day, hour=hour, minute=minute),
            text=message
        )
        return notif

# !pingme at time, message
# !pingme every time, message
# !pingme in time, message

async def initialize_time():
    now = datetime.datetime.now()
    begin = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute= now.minute + 1)
    delta = begin-now
    await sleep(delta.total_seconds())
    begin_time()

def begin_time():
    print('begin')
    check_reminders.start()

@tasks.loop(minutes=1)
async def check_reminders():
    now = datetime.datetime.now().replace(second= 0, microsecond=0)
    for notif in reminders:
        time: datetime.datetime = notif.time
        if time == now:
            reminders.remove(notif)
            await notif.send()
        else:
            break
        
        

@bot.command(aliases = ['at'])
async def _notif_at(ctx: commands.Context, *, args):
    notif = input_at_time(args, ctx)
    if notif:
        reminders.append(notif)
        await ctx.message.add_reaction('✅')

@bot.command()
async def list(ctx: commands.Context):
    if reminders:
        await reminders[0].send()
    else:
        print('empty')

@bot.command()
async def repeat(ctx: commands.Context, args):
    await ctx.send(args)

@bot.event
async def on_ready():
    print('Bot is online!')
    await initialize_time()
    
bot.run(TOKEN)