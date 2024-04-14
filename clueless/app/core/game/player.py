from clueless.app.core.game.room import Room


class Player:
    def __init__(self, name):
        self.name = name  # Player can initialize with their name
        self.character = None  # No character initialized for the player
        self.hand = []  # Player's hand of cards
        self.location = Room("Lounge")  # Player location of the board
        self.is_playing = True  # Flag if player is currently playing

    def move(self, location):
        self.location = location

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def get_player_info(self):
        print(f"Your character: {self.character.name}"
              f"\nYour location: {self.location.name}"
              f"\n{self.location.name}'s neighbors: {self.location.get_neighbors_string()}"
              f"\nCurrent Clues: " f"{self.get_hand_str()}")

    def get_hand_str(self):
        hand = []
        for card in self.hand:
            hand.append(card.name)
        return hand
