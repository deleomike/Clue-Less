import time

from clueless.app.core.game.gameboard import GameBoard
from clueless.app.core.game.hall import Hall
from clueless.app.core.game.room import Room


def print_room_neighbors(room=None, hall=None):
    idx = 0
    if room is not None:
        for neighbor in room.neighbors:
            print(f"{idx}. {neighbor.name}")
            idx += 1
    elif hall is not None:
        for neighbor in hall.neighbors:
            print(f"{idx}. {neighbor.name}")
            idx += 1


class GameLoop:
    def __init__(self):
        self.turn = 0  # Track whose turn it is
        self.board = GameBoard()  # Setup game board
        self.characters = self.board.get_characters()
        self.players = self.board.get_players()
        self.deck = self.create_deck()
        self.solution = self.select_solution()  # Random select solution
        self.game_over = False
        self.distribute_cards()
        print(self.solution)

    def create_deck(self):
        import random
        deck = []
        for character in self.characters:
            deck.append(character)
        for weapon in self.board.weapons:
            deck.append(weapon)
        for room in self.board.rooms:
            deck.append(room)
        random.shuffle(deck)
        return deck

    def select_solution(self):
        # Select a random character/weapon/room for winning solution.
        import random
        murderer = None
        crime_scene = None
        murder_weapon = None
        for card in self.deck:
            if type(card) is type(self.characters[0]):
                murderer = card
                self.deck.remove(card)
                break
        for card in self.deck:
            if type(card) is type(self.board.weapons[0]):
                murder_weapon = card
                self.deck.remove(card)
                break
        for card in self.deck:
            if type(card) is type(self.board.rooms[0]):
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

        current_player = self.players[self.turn]
        if not current_player.is_playing:
            self.turn = (self.turn + 1) % len(self.players)
            pass
        print(f"Turn: {current_player.name}")

        self.player_turn(current_player)
        # Implement game logic for each step
        # TODO Check win status and # Update game state accordingly

        # Move to the next player's turn
        self.turn = (self.turn + 1) % len(self.players)

    def player_turn(self, current_player):
        m_turn_flag = True
        print(f"\n\n{current_player.name}! It's your turn. ")
        current_player.get_player_info()
        while m_turn_flag:
            options = self.generate_options(current_player)
            print(f"\n\n{options}")
            choice = input("\nChoose an option: ")
            if choice == "0" and options.__contains__("0"):
                # move the player of character
                self.print_weapons()
                weapon_idx = int(input(f"Choose a murder weapon:"))

                self.print_characters()
                character_idx = int(input(f"Choose a killer:"))
                m_turn_flag = False
                pass
            elif choice == "1" and options.__contains__("1"):
                print_room_neighbors(room=current_player.location)
                hall_idx = int(input(f"Where to?:"))
                self.try_move(current_player, current_player.location.neighbors[hall_idx])
                m_turn_flag = False
            elif choice == "2" and options.__contains__("2"):
                print_room_neighbors(hall=current_player.location)
                room_idx = int(input(f"Where to?:"))
                self.try_move(current_player, current_player.location.neighbors[room_idx])

            elif choice == "3" and options.__contains__("3"):
                print(f"\n\nMaking an accusation, choose wisely...")

                self.print_rooms()
                room_idx = int(input(f"Choose a crime scene:"))

                self.print_weapons()
                weapon_idx = int(input(f"Choose a murder weapon:"))

                self.print_characters()
                character_idx = int(input(f"Choose a killer:"))
                m_turn_flag = False
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
        idx = 0
        for character in self.board.characters:
            print(f"{idx}. {character.name}")
            idx += 1

    def print_rooms(self):
        idx = 0
        for room in self.board.rooms:
            print(f"{idx}. {room.name}")
            idx += 1

    def generate_options(self, current_player):
        options = f""
        if type(current_player.location) is Room:
            options += f"0. Make a suggestion"
            options += f"\n1. Move to a hall"
        if type(current_player.location) is Hall:
            options += f"\n2. Move to a room"
        options += f"\n3. Make an accusation"
        return options

    def try_move(self, player, to_room):
        # Check if a move exists and is unblocked
        # Dummy example that removes game-board check (TODO)
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
                        f"{to_room.current_players.name} is in the hallway. Cannot move {player.name} to the {to_room}.")
                    return False
                else:
                    print(f"{player.name}: {player.character.name}, moved to the {to_room.name}.")
                    # player.location.current_players.remove(player)
                    to_room.current_players.append(player)
                    player.location = to_room
                    return True
        else:
            print(f"Cannot move {player.name} to the {to_room}.")
            return False

    def make_suggestion(self, player, character, weapon, room):
        # Handle suggestion logic
        print(f"Suggestion made: {character} with the {weapon} in the {room}.")
        # Move suggested character to the current room
        self.move_character(character, room)
        # Let other players respond to the suggestion (TODO)

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
        # Example setup (TODO)
        while not self.is_game_over():
            self.step()  # Player turn
            time.sleep(1)

        print(f"\n\n\n\nThanks for playing! Play again? (y/n)")
        answer = input()
        if answer.lower() == "y":
            self.run_game()
        else:
            exit(1876)


gameloop = GameLoop()
gameloop.run_game()
