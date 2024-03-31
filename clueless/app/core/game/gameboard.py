class GameBoard:
    def __init__(self):
        self.rooms = [["Study", "Hall", "Lounge"],
                      ["Library", "Billiard Room", "Dining Room"],
                      ["Conservatory", "Ballroom", "Kitchen"]]  # List of rooms on game board

        self.characters = [
            "Miss Scarlet",
            "Colonel Mustard",
            "Mrs. White",
            "Mr. Green",
            "Mrs. Peacock",
            "Professor Plum"
        ]

        self.weapons = [
            "Candlestick",
            "Knife",
            "Lead Pipe",
            "Revolver",
            "Rope",
            "Wrench"
        ]
