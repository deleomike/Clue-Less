from clueless.app.core.game.player import Player
from clueless.app.core.game.room import Room
from clueless.app.core.game.weapon import Weapon


def create_rooms():
    study = Room("Study")
    hall = Room("Hall")
    lounge = Room("Lounge")
    library = Room("Library")
    billiard_room = Room("Billiard Room")
    dining_room = Room("Dining Room")
    conservatory = Room("Conservatory")
    ball_room = Room("Ball Room")
    kitchen = Room("Kitchen")

    study.neighbors = [hall, library]
    hall.neighbors = [study, lounge, billiard_room]
    library.neighbors = [study, billiard_room, conservatory]
    billiard_room.neighbors = [hall, library, dining_room]
    dining_room.neighbors = [lounge, billiard_room, kitchen]
    conservatory.neighbors = [library, ball_room]
    ball_room.neighbors = [conservatory, kitchen]
    kitchen.neighbors = [dining_room, ball_room]

    return [study, hall, library, billiard_room, dining_room, conservatory, ball_room, kitchen]


def create_weapons():
    candlestick = Weapon("Candlestick")
    knife = Weapon("Knife")
    lead_pipe = Weapon("Lead Pipe")
    revolver = Weapon("Revolver")
    rope = Weapon("Rope")
    wrench = Weapon("Wrench")

    return [candlestick, knife, lead_pipe, revolver, rope, wrench]


def print_characters(characters):
    for i in range(len(characters)):
        print(f"{i}. {characters[i]}")


class GameBoard:
    def __init__(self):

        self.rooms = create_rooms()  # Initialize room objects and their neighbors
        self.weapons = create_weapons()  # Create list of weapon objects
        self.characters = [  # Dictionary listing character names and whether a player has selected them
            "Miss Scarlet",
            "Colonel Mustard",
            "Mrs. White",
            "Mr. Green",
            "Mrs. Peacock",
            "Professor Plum"]
        self.players = self.create_players()
        self.set_room_weapons()  # Set the locations for each weapon

    def set_room_weapons(self):  # Place weapons randomly throughout rooms
        import random
        while len(self.weapons) != 0:  # While weapons are still in the distribution array
            room_ref = random.choice(self.rooms)
            if room_ref.weapon is None:  # If a random room doesn't have a weapon put the first weapon
                # weapon in the array there
                room_ref.weapon = self.weapons.pop()
                room_ref.weapon.location = room_ref

    def create_players(self):
        players = []
        num_players = int(input("How many players are playing this game?"))
        while num_players < 2 or num_players > 6:
            num_players = int(input("2-6 players required to play Clue-Less! Enter a number between 2 & 6: "))
        for i in range(num_players):
            player = Player(f"Player {i+1}")
            player.character = self.choose_character(player)
            players.append(player)
        return players

    def choose_character(self, player):
        print("Which character do you want to be?")
        print_characters(self.characters)
        character_choice = int(input())
        while character_choice >= len(self.characters) or character_choice < 0:
            character_choice = int(input("Invalid character, please enter again."))
            print_characters(self.characters)
        print(f"{player.name} has chosen {self.characters[character_choice]}!")
        return self.characters.pop(character_choice)  # Remove at index

    def get_players(self):
        return self.players
