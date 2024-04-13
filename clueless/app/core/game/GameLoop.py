import time

from typing import List

from clueless.app.core.game.character import Character
from clueless.app.core.game.gameboard import GameBoard
from clueless.app.core.game.hall import Hall
from clueless.app.core.game.room import Room
from clueless.app.core.game.weapon import Weapon
from clueless.app.db.models.game import GameRead
from clueless.app.core.game.GameDBController import (
    GameDBController,
    GameReadWithLinks,
    CharacterReadLinks,
    CardRead,
    LocationReadLinks
)


def print_room_neighbors(locations: List[LocationReadLinks]):
    print(locations)
    rooms = [f"{idx}. {location.name}" for idx, location in enumerate(locations)]

    print("\n".join(rooms))
    # if room is not None:
    #     for neighbor in room.neighbors:
    #         print(f"{idx}. {neighbor.name}")
    #         idx += 1
    # elif hall is not None:
    #     for neighbor in hall.neighbors:
    #         print(f"{idx}. {neighbor.name}")
    #         idx += 1


def try_move(player, to_room):
    if to_room in player.location.neighbors:
        if type(player.location) is Hall:
            print(f"{player.name}: {player.character.name}, moved to the {to_room.name}.")
            player.location.current_players.remove(player)
            to_room.current_players.append(player)
            player.location = to_room
            return True
        elif type(to_room) is Hall:
            if len(to_room.current_players) > 0:
                print(
                    f"{to_room.current_players[0].name} ({to_room.current_players[0].character.name}) is in the "
                    f"hallway. Cannot move {player.name} (you) to the {to_room.name}.")
                return False
            else:
                print(f"{player.name}: {player.character.name}, moved to the {to_room.name}.")
                player.location.current_players.remove(player)
                to_room.current_players.append(player)
                player.location = to_room
                return True
    else:
        print(f"Cannot move {player.name} to the {to_room}.")
        return False


def generate_options(current_player):
    options = f""
    if "hallway" in current_player.location:
        options += f"\n3. Move to a room"
    else:
        options += f"0. Make a suggestion"
        options += f"\n1. Move to a hall"
        # if current_player.location.secret_passage is not None:
        #     options += f"\n2. Use secret passage to {current_player.location.secret_passage.name}"

    options += f"\n4. Make an accusation"
    return options


def use_secret_passage(player):
    player.location.current_players.remove(player)
    player.location = player.location.secret_passage
    player.location.current_players.append(player)
    print(f"{player.name} (you) has taken the secret passage to {player.location.name}. Shhh ;)")


def force_move_player(player, room):
    player.location.current_players.remove(player)
    player.location = room
    player.location.current_players.append(player)


class GameLoop:
    def __init__(self, game: GameRead, session):

        self.turn = 0  # Track whose turn it is
        # self.characters = self.board.get_characters()
        # self.players = self.board.get_players()
        # self.deck = self.create_deck()
        # self.solution = self.select_solution()  # select solution
        self.game_over = False
        # self.distribute_cards()

        self.controller = GameDBController(game_id=game.id, session=session)

        # print(self.solution)

    @property
    def board(self) -> GameReadWithLinks:
        return self.controller.full_state

    @property
    def players(self) -> List[CharacterReadLinks]:
        return self.board.characters

    def create_deck(self):
        import random
        deck = []
        for character in self.characters:
            deck.append(character)
        for weapon in self.board.weapons:
            deck.append(weapon)
        for room in self.board.rooms:
            deck.append(room)
        print("First shuffle...")
        random.shuffle(deck)
        
        print("Second shuffle...")
        random.shuffle(deck)
        
        print("Third shuffle...")
        random.shuffle(deck)
        return deck

    def select_solution(self):
        # Select a random character/weapon/room for winning solution.
        murderer = None
        crime_scene = None
        murder_weapon = None
        for card in self.deck:
            if type(card) is Character:
                murderer = card
                self.deck.remove(card)
                break
        for card in self.deck:
            if type(card) is Weapon:
                murder_weapon = card
                self.deck.remove(card)
                break
        for card in self.deck:
            if type(card) is Room:
                crime_scene = card
                self.deck.remove(card)
                break
        solution = {
            "character": murderer.name,
            "weapon": murder_weapon.name,
            "rooms": crime_scene.name
        }
        return solution

    def distribute_cards(self):
        print("\n\n\nDistributing cards...")
        player_idx = 0
        num_players = len(self.players)
        while len(self.deck) > 0:
            self.players[player_idx % num_players].hand.append(self.deck.pop())
            print(f"{self.players[player_idx % num_players].name} has "
                  f"{len(self.players[player_idx % num_players].hand)} cards")
            player_idx += 1

    def step(self):
        # This method would be called in a loop to progress the game
        if self.get_players_playing() < 2:
            for player in self.players:
                # TODO: is_playing field in the table
                if player.is_playing:
                    print(f"{player.user_id} ({player.name}) wins!!")
                    # TODO: Need a game over
                    self.game_over = True
                    return
        current_player = self.players[self.turn]
        if not current_player.is_playing:
            self.turn = (self.turn + 1) % len(self.players)
            return
        # Player turn entry point
        self.player_turn(current_player)
        # Move to the next player's turn
        self.turn = (self.turn + 1) % len(self.players)

    def player_turn(self, current_player: CharacterReadLinks):
        end_turn_flag = False
        print(f"\n\n{current_player.name}! It's your turn. ")
        print(self.controller.print_character_info(character_id=current_player.id))
        while not end_turn_flag:
            options = generate_options(current_player)
            print(f"{options}")
            choice = input("\nChoose an option: ")

            if choice == "0" and options.__contains__("0"):
                end_turn_flag = self.suggestion_entry(current_player)

            elif choice == "1" and options.__contains__("1"):
                adjacent = self.controller.get_adjacent_character_locations(character_id=current_player.id)
                print_room_neighbors(locations=adjacent)
                hall_idx = int(input(f"Where to?:"))
                location = adjacent[hall_idx]
                try:
                    self.controller.move_player(character_id=current_player.id, location_id=location.id)
                    end_turn_flag = True
                except Exception as e:
                    print(e)
                    end_turn_flag = False
                # end_turn_flag = try_move(current_player, current_player.location.neighbors[hall_idx])

            elif choice == "2" and options.__contains__("2"):
                print(f"Moving to secret passage...")
                use_secret_passage(current_player)
                end_turn_flag = self.suggestion_entry(current_player)

            elif choice == "3" and options.__contains__("3"):
                
                print_room_neighbors(hall=current_player.location)
                
                room_idx = int(input(f"Where to?:"))
                
                try_move(current_player, current_player.location.neighbors[room_idx])
                
                end_turn_flag = self.suggestion_entry(current_player)
                

            elif choice == "4" and options.__contains__("4"):
                print(f"\n\nMaking an accusation, choose wisely...")

                self.print_rooms()
                room_idx = int(input(f"Choose a crime scene:"))

                self.print_weapons()
                weapon_idx = int(input(f"Choose a murder weapon:"))

                self.print_characters()
                character_idx = int(input(f"Choose a killer:"))
                end_turn_flag = True
                self.make_accusation(current_player,
                                     self.board.characters[character_idx],
                                     self.board.weapons[weapon_idx],
                                     self.board.rooms[room_idx])

    def print_weapons(self):
        idx = 0
        for weapon in self.board.weapons:
            print(f"{idx}. {weapon.name}")
            idx += 1

    def print_characters(self):
        for idx, character in enumerate(self.board.characters):
            print(f"{idx}. {character.name}")

    def print_rooms(self):
        idx = 0
        for room in self.board.locations:
            print(f"{idx}. {room.name}")
            idx += 1

    def make_suggestion(self,
                        current_player: CharacterReadLinks,
                        character: str,
                        weapon: str):
        """
        Makes a suggestion

        :param current_player:
        :param character: The name of the character on the card we want to find
        :param weapon: The name of the weapon on the card we want to find
        :return:
        """

        print(f"Suggestion made: {character} with the {weapon} in the {current_player.location.name}.")

        # TODO Iterate until not None
        for next_player in self.get_next_player(): # TODO: Luke implement, maybe just in this loop

            # For each player not me, get their character object, and make suggestion
            # Get player, check if they are in the game, by index

            card: CardRead = self.controller.make_suggestion(
                current_player=current_player.id,
                accused_id=next_player.id,
                character_name=character,
                weapon_name=weapon
            )

            if card is None:
                print(f"{next_player.name} disproved the suggestion of {character}, {weapon}, {current_player.location.name}!")
            else:
                print(f"{next_player.name} gave you the {card.name} card.")
                return


    def make_accusation(self, player, character, weapon, room):
        # Check if the accusation matches the game's solution
        if self.solution == {"character": character.name, "weapon": weapon.name, "rooms": room.name}:
            print(
                f"{player.name} made the correct accusation! They win! {character.name} committed the "  # Win condition
                f"murder with the {weapon.name} in the {room.name}.")
            self.game_over = True
            return True
        else:
            print(f"{player.name} made the wrong accusation! The show goes on.")  # Handle incorrect accusation
            player.is_playing = False
            return False

    def is_game_over(self):
        return self.game_over

    def run_game(self):
        while not self.is_game_over():
            self.step()  # Player turn
            

        print(f"\n\n\n\nThanks for playing! Play again? (y/n)")
        answer = input()
        if answer.lower() == "y":
            self = GameLoop()
            self.run_game()
        else:
            exit(1876)

    def suggestion_entry(self, current_player: CharacterReadLinks):
        print(f"Making suggestion in the {current_player.location.name}...")
        # move the player of character
        self.print_weapons()
        weapon_idx = int(input(f"Suggest a murder weapon:"))

        self.print_characters()
        character_idx = int(input(f"Suggest a killer:"))

        if current_player.name == self.players[character_idx].name:
            print(f"{self.players[character_idx].name} is you! Make another suggestion")
            return self.suggestion_entry(current_player) # recurse

        self.make_suggestion(
            current_player,
            self.players[character_idx],
            self.board.weapons[weapon_idx],  # TODO wont work
        )

        return True

    def get_players_playing(self):
        count = 0
        for player in self.players:
            if player.is_playing:
                count += 1
        return count

    def get_next_player(self, current_player):
        players = []
        num_players = len(self.players)
        player_idx = self.get_player_idx(current_player)
        while self.players[player_idx + 1 % num_players] is not current_player:
            if self.players[player_idx + 1 % num_players].is_playing:
                players.append(self.players[player_idx + 1 % num_players])
                player_idx += 1
        return players

    def get_player_idx(self, current_player):
        for player_idx, player in enumerate(self.players):
            if player == current_player:
                return player_idx


if __name__ == "__main__":

    gameloop = GameLoop()
    gameloop.run_game()
