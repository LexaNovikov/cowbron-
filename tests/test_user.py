def test__init__(test_user):
    assert test_user.name == "Lexa"
    assert test_user.email == "lexa@gmail.com"
    assert test_user.role == "student"


def test_can_cancel_booking(test_user, booking):
    assert test_user.can_cancel_booking(booking) == True


def test_can_cancel_booking_error(second_user, booking):
    assert second_user.can_cancel_booking(booking) == False
