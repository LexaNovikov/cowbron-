from datetime import datetime
import pytest
from src.classes.booking import Booking


def test_init(booking, test_user, calibri):
    assert booking.room == calibri
    assert booking.user == test_user
    assert booking.start_time == datetime.strptime("12:30", "%H:%M")
    assert booking.end_time == datetime.strptime("13:30", "%H:%M")


def test_init_error(calibri, second_user):
    with pytest.raises(ValueError) as e:
        Booking(
            calibri,
            second_user,
            datetime.strptime("13:31", "%H:%M"),
            datetime.strptime("12:31", "%H:%M"),
            "active",
        )
    assert str(e.value) == "Начало интервала должно быть меньше конца интервала"


def test_str(booking):
    assert str(booking) == "Calibri, Lexa, 12:30, 13:30, active"


def test_duration(booking):
    assert booking.duration() == 60
