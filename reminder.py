from datetime import datetime
from datetime import timedelta

class Timer():

    def __init__(self, offset=None):
        #offset:
        #   weeks
        #   days
        #   hours
        #   minutes
        now = datetime.now()
        time_change = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
        self.reminder_time = now + time_change

    def get_reminder_time(self):
        return self.reminder_time

class Alarm():

    def __init__(self, date=None):
        #date:
        #   