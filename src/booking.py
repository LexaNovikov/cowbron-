import datetime
from src.room import Room
class Booking:
    def __init__(self, room:Room, user_name:str, start_time:datetime.datetime, end_time:datetime.datetime):
        if start_time>=end_time:
            raise ValueError("Начало интервала должно быть меньше конца интервала")
        self.room = room
        self.user_name = user_name
        self.start_time = start_time
        self.end_time = end_time

    def duration(self):
        return (self.end_time - self.start_time).total_seconds()//60
