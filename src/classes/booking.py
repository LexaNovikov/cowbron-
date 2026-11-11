import datetime
from src.classes.room import Room


class Booking:

    def __init__(
        self,
        room: Room,
        user,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        status: str,
    ):
        if start_time >= end_time:
            raise ValueError("Начало интервала должно быть меньше конца интервала")
        self.room = room
        self.user = user
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

    def __str__(self):
        return f"{self.room.name}, {self.user.name}, {datetime.datetime.strftime(self.start_time, "%H:%M")}, {datetime.datetime.strftime(self.end_time, "%H:%M")}, {self.status}"

    def duration(self):
        return (self.end_time - self.start_time).total_seconds() // 60
