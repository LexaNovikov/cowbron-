import pytest


def test_booking_system(booking_system):
    assert booking_system.bookings == {}
    assert booking_system._bookings_amount == 0


def test_is_available(booking_system, calibri, start_time, end_time):
    assert booking_system.is_available(calibri, start_time, end_time) == True


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
