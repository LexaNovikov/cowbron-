class Room:
    def __init__(self, name: str, capacity: int, equipment: list):
        self.name = name
        self.capacity = capacity
        self.equipment = equipment.copy()

    def add_equipment(self, equipment):
        self.equipment.append(equipment)

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        if capacity <= 0:
            raise ValueError("Вместимость комнаты должна быть больше 0")
        self._capacity = capacity

    def remove_equipment(self, equipment):
        for idx in range(len(self.equipment)):
            if self.equipment[idx] == equipment:
                self.equipment.pop(idx)
                break
