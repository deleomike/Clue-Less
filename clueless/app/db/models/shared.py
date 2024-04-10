from clueless.app.db.models.character import CharacterRead, Character
from clueless.app.db.models.location import Location, LocationRead


class CharacterReadLinks(CharacterRead):
    location: Location


class LocationReadLinks(LocationRead):
    connected_locations: list[Location]
    characters: list[Character]