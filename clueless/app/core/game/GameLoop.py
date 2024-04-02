from clueless.app.core.game.gameboard import GameBoard


def player_turn(current_player):
    pass  # TODO


class GameLoop:
    def __init__(self):
        self.turn = 0  # Track whose turn it is
        self.board = self.setup_board()  # Setup game board
        self.players = self.board.get_players()
        self.solution = self.select_solution()  # Random select solution

    def setup_board(self):
        # Initialize the gameboard
        game_board = GameBoard()
        return game_board

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
        print(f"Turn: {current_player}")

        player_turn(current_player)
        # Implement game logic for each step
        # Example action for dummy run (TODO)
        if self.move_character("Miss Scarlet", "Hallway 2"):
            print("Miss Scarlet moves to Hallway 2.")
        # Update game state accordingly

        # Move to the next player's turn
        self.turn = (self.turn + 1) % len(self.players)

    def move_character(self, character, new_position):
        # Move character to a new position if it's a legal move
        if self.is_move_legal(character, new_position):
            self.board["characters"][character] = new_position
            return True
        return False

    def is_move_legal(self, character, new_position):
        # Check if a move exists and is unblocked
        # Dummy example that removes game-board check (TODO)
        return True

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

    # Move options : Up, down, left, hallway, room etc
    # in : player
    # do : get location ->
    # out : action options

    # player.location, player.name, player.clues(list<clue>)

    def simulate_gameloop(self):
        # Example setup (TODO)
        # Dummy simulate turns (TODO)
        self.step()  # P1's turn
        self.step()  # P2's turn


gameloop = GameLoop()
gameloop.simulate_gameloop()
