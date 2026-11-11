import datetime

from src.classes.booking import Booking
from src.classes.room import Room
from src.classes.user import User


class BookingSystem:
    def __init__(self):
        self.bookings = {}
        self._bookings_amount = 0

    def is_available(
        self, room: Room, start_time: datetime.datetime, end_time: datetime.datetime
    ):
        for booking in self.bookings.values():
            if (
                booking.room == room
                and not (
                    end_time <= booking.start_time or booking.end_time <= start_time
                )
                and booking.status == "active"
            ):
                return False
        return True

    def create_booking(
        self,
        room: Room,
        user: User,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
    ):
        if self.is_available(room, start_time, end_time):
            new_booking = Booking(room, user, start_time, end_time, "active")
            self._bookings_amount += 1
            self.bookings[self._bookings_amount] = new_booking
            return new_booking
        raise ValueError("Зал уже занят на это время")

    def cancel_booking(self, booking_id, user: User):
        if self.bookings.get(booking_id) is None:
            raise ValueError("Бронирования нет в системе")
        booking = self.bookings[booking_id]
        if not (user.can_cancel_booking(booking)):
            raise PermissionError("У вас недостаточно прав для отмены бронирования")
        if not booking.status == "active":
            raise ValueError("Можно отменить только активное бронирование")
        status = "cancelled" if user == booking.user else "revoked"
        booking.status = status
        return True
