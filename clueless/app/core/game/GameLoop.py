class GameLoop:
    def __init__(self, players, characters, weapons, rooms):
        self.players = players  # List of players
        self.characters = characters  # Mapping of characters to their positions
        self.weapons = weapons  # List of weapons
        self.rooms = rooms  # List of rooms
        self.turn = 0  # Track whose turn it is
        self.board = self.setup_board()  # Setup game board
        self.solution = self.select_solution()  # Random select solution


    def setup_board(self):
        # Initialize the board layout, character starting positions, and rooms
        # Return a structure representing the board

        return {
            "rooms": {room: None for room in self.rooms},
            "hallways": {f"Hallway {i}": None for i in range(1, 10)},
            "characters": self.characters
        }

    def select_solution(self):
        # Select a random character/weapon/room for winning solution.
        # Example that removes randomness for testing (TODO)
        return {"characters": "Miss Scarlet", "weapon": "Chainsaw", "room": "Library"}

    def step(self):
        # This method would be called in a loop to progress the game

        current_player = self.players[self.turn]
        print(f"Turn: {current_player}")

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
        if self.solution == {"characters": character, "weapon" : weapon, "room": room}:
            print(f"{player} made the correct accusation! They win! {character} committed the "  # Win condition
                  f"murder with the {weapon} in the {room}.")
            return True
        else:
            print(f"{player} made the wrong accusation! The show goes on.")  # Handle incorrect accusation
            return False


# Example setup (TODO)
game = GameLoop(
    players=["Player 1", "Player 2"],
    characters={"Miss Scarlet": "Hallway 1", "Professor Plum": "Hallway 2"},
    weapons=["Gun", "Chainsaw"],
    rooms=["Kitchen", "Library"]
)


# Dummy simulate turns (TODO)
game.step()  # P1's turn
game.step()  # P2's turn
