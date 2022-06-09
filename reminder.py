from datetime import datetime
from datetime import timedelta

class Notification():
    def __init__(self, time: datetime, message: str, repeating: bool, recipients: list):
        self.time: datetime = time
        self.message: str = message
        self.repeating: bool = repeating

    def __fire():
        pass

