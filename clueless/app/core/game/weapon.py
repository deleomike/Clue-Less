class Weapon:
    def __init__(self, name):
        self.name = name
        self.location = None  # Location of weapon on gameboard
        self.is_active = True  # Flag whether weapon is in play

    def move(self, location):
        if self.is_active:
            self.location = location
        else:
            print("Weapon not in play, can't move")

    def deactivate(self):
        self.is_active = False



