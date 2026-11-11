from datetime import datetime

import pytest
def to_dt(time:str):
    return datetime.strptime(time, "%H:%M")

def test_booking_system(booking_system):
    assert booking_system.bookings == {}
    assert booking_system._bookings_amount == 0

@pytest.mark.parametrize("start_timing, end_timing, expected_available", [(to_dt("12:30"), to_dt("13:30"), False),
                                                                   (to_dt("13:30"), to_dt("14:30"), True),
                                                                   (to_dt("12:00"), to_dt("13:00"), False),
                                                                   (to_dt("12:29"), to_dt("12:31"), False),
                                                                   (to_dt("13:00"), to_dt("14:00"), False),
                                                                   (to_dt("11:00"), to_dt("14:00"), False),
                                                                   (to_dt("12:40"), to_dt("13:20"), False),
                                                                       (to_dt("11:30"), to_dt("12:30"), True)])
def test_is_available(start_timing, end_timing, expected_available ,bs, test_user, calibri):
    assert bs.is_available(calibri, start_timing, end_timing) == expected_available


def test_is_available_with_error(
    booking_system, calibri, test_user, start_time, end_time
):
    booking_system.create_booking(calibri, test_user, start_time, end_time)

    assert booking_system.is_available(calibri, start_time, end_time) == False


def test_create_booking(booking_system, test_user, calibri, start_time, end_time):
    assert (
        booking_system.create_booking(calibri, test_user, start_time, end_time).room
        == calibri
    )
    assert booking_system._bookings_amount == 1


def test_create_booking_with_error(
    booking_system, test_user, calibri, start_time, end_time
):
    booking_system.create_booking(calibri, test_user, start_time, end_time)
    with pytest.raises(ValueError) as e:
        booking_system.create_booking(calibri, test_user, start_time, end_time)
    assert str(e.value) == "Зал уже занят на это время"


def test_cancel_booking(booking_system, test_user, calibri, start_time, end_time):
    assert (
        booking_system.create_booking(calibri, test_user, start_time, end_time).room
        == calibri
    )
    assert booking_system.cancel_booking(1, test_user) == True
    assert booking_system.bookings[1].status == "cancelled"


def test_revoke_booking(
    booking_system, test_user, calibri, start_time, end_time, curator
):
    booking_system.create_booking(calibri, test_user, start_time, end_time)
    assert booking_system.cancel_booking(1, curator) == True
    assert booking_system.bookings[1].status == "revoked"


def test_cancel_booking_value_error(
    booking_system, test_user, calibri, start_time, end_time
):
    with pytest.raises(ValueError) as e:
        booking_system.cancel_booking(1, test_user)
    assert str(e.value) == "Бронирования нет в системе"
    booking_system.create_booking(calibri, test_user, start_time, end_time)
    booking_system.cancel_booking(1, test_user)
    with pytest.raises(ValueError) as e:
        booking_system.cancel_booking(1, test_user)
    assert str(e.value) == "Можно отменить только активное бронирование"


def test_cancel_booking_permission_error(
    booking_system, test_user, second_user, calibri, start_time, end_time
):
    booking_system.create_booking(calibri, test_user, start_time, end_time)
    with pytest.raises(PermissionError) as e:
        booking_system.cancel_booking(1, second_user)
    assert str(e.value) == "У вас недостаточно прав для отмены бронирования"

def test_student_cannot_cancel_revoked_booking(bs, curator, test_user):
    bs.cancel_booking(1, curator)
    assert bs.bookings[1].status == "revoked"
    with pytest.raises(ValueError) as e:
        bs.cancel_booking(1, test_user)
    assert str(e.value) == "Можно отменить только активное бронирование"
    assert bs.bookings[1].status == "revoked"

def test_curator_cannot_revoke_cancelled_booking(bs, curator, test_user):
    bs.cancel_booking(1, test_user)
    assert bs.bookings[1].status == "cancelled"
    with pytest.raises(ValueError) as e:
        bs.cancel_booking(1, curator)
    assert str(e.value) == "Можно отменить только активное бронирование"
    assert bs.bookings[1].status == "cancelled"
@pytest.mark.parametrize(
    "status, role", [("cancelled", "student"), ("revoked", "curator")]
)
def test_cancelled_or_revoked_booking_releases_room(calibri, bs,status, role, curator, test_user, start_time, end_time):
    if role == "curator":
        user = curator
    elif role == "student":
        user = test_user
    bs.cancel_booking(1, user)
    assert bs.bookings[1].status == status
    assert bs.is_available(calibri, start_time, end_time)
