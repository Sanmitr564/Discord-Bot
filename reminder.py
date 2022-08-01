from datetime import datetime
from datetime import timedelta
import discord
from discord.ext import commands

class Notification():
    def __init__(self, ctx: commands.Context, time: datetime, text: str = "", repeating: bool = False):
        self.ctx: commands.Context = ctx
        self.time: datetime = time
        self.text: str = text
        self.repeating: bool = repeating
        self.recipients: list[discord.User] = [ctx.author]

    async def send(self):
        message = ""
        for r in self.recipients:
            message += f"<@{r.id}> "
        message += self.text
        await self.ctx.send(message)
    