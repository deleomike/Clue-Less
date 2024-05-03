class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player_name):
        if(player_name in self.players):
            print("Player name already taken, please pick a new one")
        elif(len(self.players) >= 6):
            print("Max number of players already reached, cannot add anymore")
        else:
            print("PlayerManager - add_player(),", player_name)
            self.players.append(player_name)

    def get_players(self):
        print("PlayerManager - get_players(), players = ",self.players)
        return self.players