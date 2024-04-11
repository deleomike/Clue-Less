from clueless.app.db.models.character import CharacterRead, Character
from clueless.app.db.models.game import GameRead
from clueless.app.db.models.card import Card
from clueless.app.db.models.location import Location, LocationRead


class CharacterReadLinks(CharacterRead):
    location: Location
    hand: list[Card] = None


class LocationReadLinks(LocationRead):
    connected_locations: list[Location]
    characters: list[Character]


class GameReadWithLinks(GameRead):
    locations: list[LocationReadLinks]
    characters: list[CharacterRead] = None
    solution: list[Card] = None