from clueless.app.core.game.character import Character
from clueless.app.core.game.player import Player
from clueless.app.core.game.room import Room
from clueless.app.core.game.weapon import Weapon
from clueless.app.core.game.hall import Hall


def create_rooms_and_halls():
    study = Room("Study")
    hall = Room("Hall")
    lounge = Room("Lounge")
    library = Room("Library")
    billiard_room = Room("Billiard Room")
    dining_room = Room("Dining Room")
    conservatory = Room("Conservatory")
    ballroom = Room("Ballroom")
    kitchen = Room("Kitchen")

    sh_hall = Hall("Study-Hallway Hall")
    hl_hall = Hall("Hall-Lounge Hall")
    sl_hall = Hall("Study-Lounge Hall")
    lb_hall = Hall("Lounge-Billiard Room Hall")
    bd_hall = Hall("Billiard Room-Dining Room Hall")
    hb_hall = Hall("Hall-Billiard Room Hall")
    ld_hall = Hall("Lounge-Dining Room Hall")
    lc_hall = Hall("Library-Conservatory Hall")
    cb_hall = Hall("Conservatory-Ballroom Hall")
    bb_hall = Hall("Billiard Room-Ballroom Hall")
    dk_hall = Hall("Dining Room-Kitchen Hall")
    bk_hall = Hall("Ballroom-Kitchen Hall")

    study.neighbors = [sl_hall, sh_hall]
    hall.neighbors = [sh_hall, hl_hall, hb_hall]
    lounge.neighbors = [hl_hall, ld_hall]
    library.neighbors = [sl_hall, lb_hall, lc_hall]
    billiard_room.neighbors = [hb_hall, lb_hall, ld_hall]
    dining_room.neighbors = [ld_hall, bd_hall, dk_hall]
    conservatory.neighbors = [lc_hall, cb_hall]
    ballroom.neighbors = [bb_hall, cb_hall, bk_hall]
    kitchen.neighbors = [dk_hall, bk_hall]

    study.secret_passage = kitchen
    kitchen.secret_passage = study

    lounge.secret_passage = conservatory
    conservatory.secret_passage = lounge

    sl_hall.neighbors = [study, library]
    sh_hall.neighbors = [study, hall]
    hl_hall.neighbors = [hall, lounge]
    hb_hall.neighbors = [hall, billiard_room]
    ld_hall.neighbors = [lounge, dining_room]
    lb_hall.neighbors = [library, billiard_room]
    bd_hall.neighbors = [billiard_room, dining_room]
    lc_hall.neighbors = [library, conservatory]
    bb_hall.neighbors = [billiard_room, ballroom]
    dk_hall.neighbors = [dining_room, kitchen]
    cb_hall.neighbors = [conservatory, ballroom]
    bk_hall.neighbors = [ballroom, kitchen]

    return [study, hall, lounge,
            library, billiard_room, dining_room,
            conservatory, ballroom, kitchen,
            sh_hall, hl_hall,
            sl_hall, hb_hall, ld_hall,
            lb_hall, bd_hall,
            lc_hall, bb_hall, dk_hall,
            cb_hall, bk_hall]


def create_weapons():
    candlestick = Weapon("Candlestick")
    knife = Weapon("Knife")
    lead_pipe = Weapon("Lead Pipe")
    revolver = Weapon("Revolver")
    rope = Weapon("Rope")
    wrench = Weapon("Wrench")

    return [candlestick, knife, lead_pipe, revolver, rope, wrench]


def create_characters():
    miss_scarlet = Character("Miss Scarlet")
    colonel_mustard = Character("Colonel Mustard")
    mrs_white = Character("Mrs. White")
    mr_green = Character("Mr. Green")
    mrs_peacock = Character("Mrs. Peacock")
    professor_plum = Character("Professor Plum")
    return [miss_scarlet, colonel_mustard, mrs_white, mrs_peacock, professor_plum, mr_green]


def print_characters(characters):
    for i in range(len(characters)):
        print(f"{i}. {characters[i].name}")


class GameBoard:
    def __init__(self):
        self.locations = create_rooms_and_halls()
        self.rooms = self.locations[0:9]
        self.halls = self.locations[9:]
        self.weapons = create_weapons()  # Create list of weapon objects
        self.characters = create_characters()
        self.players = self.create_players()
        self.set_player_locations()

    def create_players(self):
        players = []
        num_players = int(input("How many players are playing this game?"))
        while num_players < 2 or num_players > 6:
            num_players = int(input("2-6 players required to play Clue-Less! Enter a number between 2 & 6: "))
        for i in range(num_players):
            player = Player(f"Player {i + 1}")
            player.character = self.choose_character(player)
            players.append(player)
        self.characters = create_characters()
        return players

    def set_player_locations(self):

        # sh_hall, hl_hall,
        # sl_hall, hb_hall, ld_hall,
        # lb_hall, bd_hall,
        # lc_hall, bb_hall, dk_hall,
        # cb_hall, bk_hall
        num_players = len(self.players)
        if num_players == 6:
            self.players[0].location = self.halls[2]
            self.players[0].location.current_players.append(self.players[0])
            self.players[1].location = self.halls[7]
            self.players[1].location.current_players.append(self.players[1])
            self.players[2].location = self.halls[10]
            self.players[2].location.current_players.append(self.players[2])
            self.players[3].location = self.halls[11]
            self.players[3].location.current_players.append(self.players[3])
            self.players[4].location = self.halls[4]
            self.players[4].location.current_players.append(self.players[4])
            self.players[5].location = self.halls[1]
            self.players[5].location.current_players.append(self.players[5])
        elif num_players == 5:
            self.players[0].location = self.halls[2]
            self.players[0].location.current_players.append(self.players[0])
            self.players[1].location = self.halls[7]
            self.players[1].location.current_players.append(self.players[1])
            self.players[2].location = self.halls[10]
            self.players[2].location.current_players.append(self.players[2])
            self.players[3].location = self.halls[11]
            self.players[3].location.current_players.append(self.players[3])
            self.players[4].location = self.halls[4]
            self.players[4].location.current_players.append(self.players[4])
        elif num_players == 4:
            self.players[0].location = self.halls[2]
            self.players[0].location.current_players.append(self.players[0])
            self.players[1].location = self.halls[7]
            self.players[1].location.current_players.append(self.players[1])
            self.players[2].location = self.halls[10]
            self.players[2].location.current_players.append(self.players[2])
            self.players[3].location = self.halls[11]
            self.players[3].location.current_players.append(self.players[3])
        elif num_players == 3:
            self.players[0].location = self.halls[2]
            self.players[0].location.current_players.append(self.players[0])
            self.players[1].location = self.halls[7]
            self.players[1].location.current_players.append(self.players[1])
            self.players[2].location = self.halls[10]
            self.players[2].location.current_players.append(self.players[2])
        elif num_players == 2:
            self.players[0].location = self.halls[2]
            self.players[0].location.current_players.append(self.players[0])
            self.players[1].location = self.halls[7]
            self.players[1].location.current_players.append(self.players[1])

    def choose_character(self, player):
        print("Which character do you want to be?")
        print_characters(self.characters)
        character_choice = int(input())
        while character_choice >= len(self.characters) or character_choice < 0:
            character_choice = int(input("Invalid character, please enter again."))
            print_characters(self.characters)
        print(f"{player.name} has chosen {self.characters[character_choice].name}!")
        return self.characters.pop(character_choice)  # Remove at index

    def get_players(self):
        return self.players

    def get_characters(self):
        return self.characters
