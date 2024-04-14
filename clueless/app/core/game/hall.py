class Hall:
    def __init__(self, name):
        self.name = name
        self.current_players = []
        self.neighbors = []

    def get_neighbors(self):  # Get locations next to current hallway
        return self.neighbors

    def add_player(self, player):  # Add player to a room
        self.current_players.append(player)

    def remove_player(self, player):  # Remove player from a room
        self.current_players.remove(player)

    def is_neighbor(self, room):
        return True if room in self.neighbors else False

    def get_neighbors_string(self):
        neighbors = []
        for neighbor in self.neighbors:
            neighbors.append(neighbor.name)
        return neighbors
