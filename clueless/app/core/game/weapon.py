class Weapon:
    def __init__(self, name):
        self.name = name  # Weapon name ie 'Revolver'
        self.location = None  # Location of weapon on game board
        self.is_active = True  # Flag whether weapon is in play

    def move(self, location):  # Move weapon to another location if needed
        if self.is_active:
            self.location = location
        else:
            print("Weapon not in play, can't move")

    def deactivate(self):  # Deactivate weapon
        self.is_active = False
