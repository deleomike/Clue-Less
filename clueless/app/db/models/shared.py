from clueless.app.db.models.character import CharacterRead, Character
from clueless.app.db.models.game import GameRead
from clueless.app.db.models.card import CardRead
from clueless.app.db.models.location import Location, LocationRead


class CharacterReadLinks(CharacterRead):
    location: LocationRead
    hand: list[CardRead] = None


class LocationReadLinks(LocationRead):
    connected_locations: list[LocationRead]
    characters: list[CharacterRead]


class GameReadWithLinks(GameRead):
    locations: list[LocationReadLinks]
    characters: list[CharacterRead] = None
    solution: list[CardRead] = None


class CardReadWithLinks(CardRead):
    characters: list[CharacterRead]
