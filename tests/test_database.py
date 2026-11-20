import datetime

import pytest

from src.database.booking import create_booking, to_datetime


def test_to_datetime() -> None:
    assert to_datetime('2026-11-21', '14:40') == datetime.datetime(2026,11,21,14,40)
def test_to_datetime_error() -> None:
    with pytest.raises(ValueError) as e:
        to_datetime('piska', '')
    assert str(e.value) == "time data 'piska ' does not match format '%Y-%m-%d %H:%M'"
def test_create_booking_409() -> None:
    with pytest.raises(ValueError) as e:
        create_booking(4, 1, '2026-11-21', '14:00', '15:00')
    assert str(e.value) == "409 Conflict: Аудитория уже занята"
def test_create_booking_201() -> None:

    assert create_booking(4, 1, '2026-11-21', '18:00', '19:00') == 9

def test_create_booking_404_room() -> None:
    with pytest.raises(ValueError) as e:
        create_booking(12, 1, '2026-11-21', '14:00', '15:00')
    assert str(e.value) == "404 Not Found: Выбранной комнаты не существует"
def test_create_booking_404_user() -> None:
    with pytest.raises(ValueError) as e:
        create_booking(4, 999, '2026-11-21', '14:00', '15:00')
    assert str(e.value) == "404 Not Found: Пользователя не существует"
def test_create_booking_400() -> None:
    with pytest.raises(ValueError) as e:
        create_booking(12, 1, '2026-11-21', '15:00', '14:00')
    assert str(e.value) == "400 Bad Request: Конец бронирования должен быть позже начала"


