import pytest
from src.classes.user import User
from src.classes.room import Room
from src.classes.booking import Booking
from src.classes.booking_system import BookingSystem
import datetime


@pytest.fixture
def test_user():
    return User("Lexa", "lexa@gmail.com", "student")


@pytest.fixture
def second_user():
    return User("Lena", "lena@gmail.com", "student")


@pytest.fixture
def calibri():
    return Room("Calibri", 56, [])


@pytest.fixture
def booking(calibri, test_user):
    return Booking(
        calibri,
        test_user,
        datetime.datetime.strptime("12:30", "%H:%M"),
        datetime.datetime.strptime("13:30", "%H:%M"),
        "active",
    )


@pytest.fixture
def second_booking(calibri, second_user):
    return Booking(
        calibri,
        second_user,
        datetime.datetime.strptime("12:31", "%H:%M"),
        datetime.datetime.strptime("13:31", "%H:%M"),
        "active",
    )


@pytest.fixture
def booking_system():
    return BookingSystem()



@pytest.fixture
def start_time():
    return datetime.datetime.strptime("12:30", "%H:%M")


@pytest.fixture
def end_time():
    return datetime.datetime.strptime("13:30", "%H:%M")


@pytest.fixture
def curator():
    return User("Polina", "polina@gmail.com", "curator")


@pytest.fixture
def bs(calibri, test_user, start_time, end_time):
    bs = BookingSystem()
    bs.create_booking(calibri, test_user, start_time, end_time)
    return bs