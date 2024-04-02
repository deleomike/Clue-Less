class Room:
    def __init__(self, name):
        self.name = name
        self.current_players = []
        self.neighbors = None
        self.weapon = None

    def get_neighbors(self):  # Get rooms one hallway away from current room
        return self.neighbors

    def add_player(self, player):  # Add player to a room
        self.current_players.append(player)

    def remove_player(self, player):  # Remove player from a room
        self.current_players.remove(player)

    def get_weapons(self):  # Get weapon in room, if any
        return self.weapon

    def is_neighbor(self, room):
        return True if room in self.neighbors else False
