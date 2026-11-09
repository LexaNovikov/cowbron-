class Room:
    def __init__(self, name:str, capacity:int, equipment:list):
        self.name = name
        self.capacity = capacity
        self.equipment = equipment.copy()
    def add_equipment(self, equipment):
        self.equipment.append(equipment)
    def remove_equipment(self, equipment):
        for idx in range(len(self.equipment)):
            if self.equipment[idx] == equipment:
                self.equipment.pop(idx)
                break

