import time

from typing import List

from clueless.app.db.models.character import CharacterRead, Character
from clueless.app.db.models.game import GameRead
from clueless.app.core.game.GameDBController import (
    GameDBController,
    GameReadWithLinks,
    CharacterReadLinks,
    CardRead,
    LocationReadLinks
)
from clueless.app.db.models.location import LocationRead


def print_room_neighbors(locations: List[LocationRead]):
    rooms = [f"{idx}. {location.name}" for idx, location in enumerate(locations)]
    print("\n".join(rooms))

def use_secret_passage(player):
    player.location_id.current_players.remove(player)
    player.location_id = player.location_id.secret_passage
    player.location_id.current_players.append(player)
    print(f"{player.name} (you) has taken the secret passage to {player.location_id.name}. Shhh ;)")


def force_move_player(player, room):
    player.location.current_players.remove(player)
    player.location = room
    player.location.current_players.append(player)


class GameLoop:
    def __init__(self, game: GameRead, session):
        self.turn = 0  # Track whose turn it is
        self.game_over = False

        self.controller = GameDBController(game_id=game.id, session=session)

        print(
            f"SOLUTION: {self.controller.solution[0].name}, {self.controller.solution[1].name}, {self.controller.solution[2].name}")


    @property
    def board(self) -> GameReadWithLinks:
        return self.controller.full_state

    @property
    def players(self) -> List[CharacterReadLinks]:
        return self.board.characters

    def _format_string_list(self, string_list: List[str]) -> str:
        """
        adds input ids

        :param string_list:
        :return:
        """

        names = [f"{idx}. {name}" for idx, name in enumerate(string_list)]

        return "\n".join(names)

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

    def generate_options(self, current_player):
        options = f""
        if "-" in current_player.location.name:
            options += f"\n3. Move to a room"
        else:
            options += f"0. Make a suggestion"
            options += f"\n1. Move to a hall"
            neighbors = self.controller.get_adjacent_locations(
                current_player.location.id)
            if len(neighbors) > 2 and "-" not in neighbors[2].name:
                options += f"\n2. Use secret passage to {neighbors[2]}"

        options += f"\n4. Make an accusation"
        return options

    def step(self):
        # This method would be called in a loop to progress the game
        if self.get_players_playing() < 2:
            for player in self.players:

                if player.is_playing:
                    print(f"{player.user_id} ({player.name}) wins!!")
                    # TODO: Need a game over (think this is done)
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
            options = self.generate_options(current_player)
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
                    print(location)
                    end_turn_flag = True  # TODO IF ITS A ROOM/SECRET PASSAGE GIVE ABILITY TO SUGGEST
                except Exception as e:
                    print(e)
                    end_turn_flag = False
                # end_turn_flag = try_move(current_player, current_player.location.neighbors[hall_idx])

            elif choice == "2" and options.__contains__("2"):
                print(f"Moving to secret passage...")
                use_secret_passage(current_player)
                end_turn_flag = self.suggestion_entry(current_player)

            elif choice == "3" and options.__contains__("3"):

                neighbors = self.controller.get_adjacent_locations(current_player.location_id)
                print_room_neighbors(
                    locations=neighbors)

                room_idx = int(input(f"Where to?:"))
                location = neighbors[room_idx]

                try:
                    self.controller.move_player(character_id=current_player.id, location_id=location.id)
                    print(f"{current_player.name} moved to {location.name}.")
                    end_turn_flag = self.suggestion_entry(current_player)
                except Exception as e:
                    print(e)

                # try_move(current_player, current_player.location.neighbors[room_idx])



            elif choice == "4" and options.__contains__("4"):
                print(f"\n\nMaking an accusation, choose wisely...")

                self.print_rooms()
                room_idx = int(input(f"Choose a crime scene:"))

                self.print_weapons()
                weapon_idx = int(input(f"Choose a murder weapon:"))

                self.print_characters()
                character_idx = int(input(f"Choose a killer:"))
                end_turn_flag = True
                self.make_accusation(
                    current_player,
                    self.controller.character_card_list[character_idx],
                    self.controller.weapon_card_list[weapon_idx],
                    self.controller.location_card_list[room_idx]
                )

    def print_weapons(self):
        print(self._format_string_list(self.controller.weapon_card_list))

    def print_characters(self):
        print(self._format_string_list(self.controller.character_card_list))

    def print_rooms(self):
        print(self._format_string_list(self.controller.location_card_list))

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

        # print("ENTERING FUNCTION")

        print(f"Suggestion made: {character} with the {weapon} in the {current_player.location.name}.")
        if character == current_player.name:
            print("Suggesting yourself huh? Could it really be you?")
        else:
            print(f"{character} has been called into the {current_player.location.name}...")

            suggested_player = self.find_by_name(character)

            if "-" in current_player.location.name:
                raise Exception("Cannot make a suggestion from a hallway")
            # teleport the accused
            if type(suggested_player) is Character:
                # print("Trying to move player")
                self.controller.move_player(character_id=suggested_player.id,
                                            location_id=current_player.location_id,
                                            validate=False)

        for next_player in self.get_next_player(current_player=current_player):

            # For each player not me, get their character object, and make suggestion
            # Get player, check if they are in the game, by index
            # print("LOOPING")

            print("CHARACTER CHOSEN: ", character)

            card: CardRead = self.controller.make_suggestion(
                current_player=current_player.id,
                accused_id=next_player.id,
                character_name=character,
                weapon_name=weapon
            )

            if card is None:
                print(
                    f"{next_player.name} disproved the suggestion of {character}, {weapon}, {current_player.location.name}!")
            else:
                print(f"{next_player.name} showed you the {card.name} card.")
                return

    def find_by_name(self, character_name: str) -> CharacterRead | None:
        for player in self.controller.players:
            if player.name == character_name:
                return player
        return None

    def make_accusation(self, player: CharacterReadLinks, character: str, weapon: str, room: str):
        # Check if the accusation matches the game's solution
        result = self.controller.make_accusation(
            current_player_id=player.id,
            room_name=room,
            weapon=weapon,
            player_name=character
        )
        if result:
            print(
                f"{player.name} made the correct accusation! They win! {character} committed the "  # Win condition
                f"murder with the {weapon} in the {room}.")
            self.game_over = True
            return True
        else:
            print(f"{player.name} made the wrong accusation! The show goes on.")  # Handle incorrect accusation
            player.is_playing = False
            return False

    def is_game_over(self):
        return self.board.game_over

    def run_game(self):
        while not self.is_game_over():
            self.step()  # Player turn

        print(f"\n\n\n\nThanks for playing! Play again? (y/n)")  # TODO BROKEN
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

        character_name = self.controller.character_card_list[character_idx]

        self.make_suggestion(
            current_player=current_player,
            character=character_name,
            weapon=self.controller.weapon_card_list[weapon_idx],  # TODO wont work
        )

        return True

    def get_players_playing(self):
        count = 0
        for player in self.players:
            if player.is_playing:
                count += 1
        return count

    def get_next_player(self, current_player):

        from copy import deepcopy

        current_player_index = self.get_player_idx(current_player=current_player)

        in_order_players = deepcopy(self.players[current_player_index:])
        in_order_players.extend(self.players[:current_player_index])

        for player in in_order_players:
            if player.id == current_player.id:
                continue

            yield player

    def get_player_idx(self, current_player):
        for player_idx, player in enumerate(self.players):
            if player == current_player:
                return player_idx


if __name__ == "__main__":
    gameloop = GameLoop()
    gameloop.run_game()
