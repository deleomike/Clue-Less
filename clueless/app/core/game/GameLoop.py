import time

from clueless.app.core.game.gameboard import GameBoard


class GameLoop:
    def __init__(self):
        self.turn = 0  # Track whose turn it is
        self.board = GameBoard()  # Setup game board
        self.players = self.board.get_players()
        self.solution = self.select_solution()  # Random select solution
        self.game_over = False

    def select_solution(self):
        # Select a random character/weapon/room for winning solution.
        import random
        murderer = random.choice(self.players)
        crime_scene = random.choice(self.board.rooms)
        murder_weapon = random.choice(self.board.rooms).weapon
        solution = {
            "character": murderer.character,
            "weapon": murder_weapon,
            "rooms": crime_scene
        }
        return solution

    def step(self):
        # This method would be called in a loop to progress the game

        current_player = self.players[self.turn]
        print(f"Turn: {current_player.name}")

        self.player_turn(current_player)
        # Implement game logic for each step
        # TODO Check win status and # Update game state accordingly

        # Move to the next player's turn
        self.turn = (self.turn + 1) % len(self.players)

    def move_character(self, player, room):
        # Move character to a new position if it's a legal move
        if self.is_move_legal(player, room):
            # TODO Move player to room by setting player location and room current players
            return True
        return False

    def player_turn(self, current_player):
        pass  # TODO

    def is_move_legal(self, player, to_room):
        # Check if a move exists and is unblocked
        # Dummy example that removes game-board check (TODO)
        if to_room in player.location.neighbors:
            print(f"{player.name}: {player.character}, moved to the {to_room}.")
            player.location.current_players.remove(player)
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
        if self.solution == {"characters": character, "weapon": weapon, "room": room}:
            print(f"{player} made the correct accusation! They win! {character} committed the "  # Win condition
                  f"murder with the {weapon} in the {room}.")
            return True
        else:
            print(f"{player} made the wrong accusation! The show goes on.")  # Handle incorrect accusation
            return False

    def is_game_over(self):
        return self.game_over

    # Move options : Up, down, left, hallway, room etc
    # in : player
    # do : get location ->
    # out : action options

    # player.location, player.name, player.clues(list<clue>)

    def run_game(self):
        # Example setup (TODO)
        while 1:
            self.step()  # Player turn
            time.sleep(1)

            if self.is_game_over():
                break


gameloop = GameLoop()
gameloop.run_game()
