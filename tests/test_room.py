import pytest


def test_init(calibri):
    assert calibri.name == "Calibri"
    assert calibri.capacity == 56
    assert calibri.equipment == []


def test_add_equipment(calibri):
    calibri.add_equipment("equipment")
    assert calibri.equipment == ["equipment"]


def test_capacity(calibri):
    assert calibri.capacity == 56


def test_set_capacity(calibri):
    calibri.capacity = 58
    assert calibri.capacity == 58


def test_set_capacity_error(calibri):
    with pytest.raises(ValueError) as e:
        calibri.capacity = 0
    assert str(e.value) == "Вместимость комнаты должна быть больше 0"


def test_remove_equipment(calibri):
    calibri.add_equipment("equipment")
    calibri.remove_equipment("equipment")
    assert calibri.equipment == []
