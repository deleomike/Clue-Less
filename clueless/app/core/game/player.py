class Player:
    def __init__(self, name):
        self.name = name  # Player can initialize with their name
        self.character = None  # No character initialized for the player
        self.hand = []  # Player's hand of cards
        self.location = None  # Player location of the board
        self.is_playing = True  # Flag if player is currently playing

    def move(self, location):
        self.location = location

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)

