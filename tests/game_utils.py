from fastapi.testclient import TestClient
from typing import Dict, List

from clueless.app.db.models.shared import GameReadWithLinks, CharacterReadLinks, LocationReadLinks, LocationRead
from clueless.app.core.schemas.game import suggestion_response
from clueless.app.db.models.card import CardRead

def get_character(game_id, test_client: TestClient, headers: Dict) -> CharacterReadLinks:
    response = test_client.get(
        f"/api/game/{game_id}/character/",
        headers=headers
    ).json()

    return CharacterReadLinks.model_validate(response)


def start_game(room_id, test_client: TestClient, headers: Dict) -> GameReadWithLinks:
    response = test_client.post(
        f"/api/room/{room_id}/start",
        headers=headers
    ).json()

    return GameReadWithLinks.model_validate(response)


def valid_moves(game_id, test_client: TestClient, headers: Dict) -> List[LocationRead]:
    response = test_client.post(
        f"/api/game/{game_id}/character/valid_moves",
        headers=headers
    ).json()

    result = [LocationRead.model_validate(data) for data in response]

    return result

def move_character(game_id, location_id, test_client: TestClient, headers: Dict) -> CharacterReadLinks:

    response = test_client.post(
        f"/api/game/{game_id}/character/move/{location_id}",
        headers=headers
    ).json()

    return CharacterReadLinks.model_validate(response)

def make_suggestion(
        game_id,
        character_name,
        weapon_name,
        test_client: TestClient,
        headers: Dict
) -> suggestion_response:

    response = test_client.post(
        f"/api/game/{game_id}/character/make_suggestion",
        headers=headers,
        json={
            "character_name": character_name,
            "weapon_name": weapon_name,
        }
    ).json()

    return CardRead.model_validate(response)


def make_accusation(
        game_id,
        character_name,
        weapon_name,
        room_name,
        test_client: TestClient,
        headers: Dict
) -> bool:

    response = test_client.post(
        f"/api/game/{game_id}/character/make_accusation",
        headers=headers,
        json={
            "character_name": character_name,
            "weapon_name": weapon_name,
            "room_name": room_name
        }
    ).json()

    print("RESPONSE ", response)

    return response["win"]

