from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from clueless.app.db.models.game import GameRead, GameCreate, GameUpdate
from clueless.app.db.models.location import LocationRead
from clueless.app.db.models.character import CharacterRead
from clueless.app.db.models.card import CardRead
from clueless.app.db.models.shared import GameReadWithLinks, CharacterReadLinks, LocationReadLinks
from clueless.app.core.game.GameDBController import GameDBController
from clueless.app.db.crud.game import GameCRUD
from clueless.app.db import get_session
from clueless.app.core.users import current_active_user
from clueless.app.core.schemas.game import suggestion_response, SuggestionRequest, AccusationRequest


router = APIRouter()


@router.get("/", response_model=List[GameRead])
async def get_all(crud: GameCRUD = Depends(GameCRUD.as_dependency)):
    return crud.get_all()


@router.get("/{_id}/", response_model=GameReadWithLinks)
async def get_game_info(_id: UUID,
                  crud: GameCRUD = Depends(GameCRUD.as_dependency)):
    """
    Gets the game by either the alphanumeric game key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    return crud.get(_id)


@router.get("/{_id}/character/", response_model=CharacterReadLinks)
async def get_character(_id: UUID,
                  crud: GameCRUD = Depends(GameCRUD.as_dependency),
                  user = Depends(current_active_user)):
    """
    Gets the character info for the user
    :param _id:
    :param crud:
    :return:
    """
    controller = GameDBController(game_id=_id, session=crud.session)
    return controller.get_character_info(user_id=user.id)


@router.post("/{_id}/character/valid_moves/", response_model=List[LocationRead])
async def valid_moves(_id: UUID,
                crud: GameCRUD = Depends(GameCRUD.as_dependency),
                user = Depends(current_active_user)):
    """
    Gets list of valid locations to move to

    :param _id:
    :param crud:
    :param user:
    :return:
    """
    controller = GameDBController(game_id=_id, session=crud.session)
    character = controller.get_character_info(user_id=user.id)

    return controller.get_adjacent_character_locations(character_id=character.id)


@router.post("/{_id}/character/move/{location_id}", response_model=CharacterReadLinks)
async def move_character(_id: UUID,
                  location_id: UUID,
                  crud: GameCRUD = Depends(GameCRUD.as_dependency),
                  user = Depends(current_active_user)):
    """
    Moves the character

    :param _id:
    :param location_id:
    :param crud:
    :param user:
    :return:
    """
    controller = GameDBController(game_id=_id, session=crud.session)
    character = controller.get_character_info(user_id=user.id)

    return controller.move_player(character_id=character.id, location_id=location_id, validate=True)



@router.post("/{_id}/character/make_suggestion", response_model=CardRead)
async def make_suggestion(_id: UUID,
                          request: SuggestionRequest,
                          crud: GameCRUD = Depends(GameCRUD.as_dependency),
                          user = Depends(current_active_user)):
    """
    Make a suggestion, teleports the suggested player

    :param _id:
    :param accused_player_id:
    :param weapon:
    :param crud:
    :param user:
    :return:
    """
    controller = GameDBController(game_id=_id, session=crud.session)
    character = controller.get_character_info(user_id=user.id)

    card = controller.make_suggestions(
        current_player_id=character.id,
        character_name=request.character_name,
        weapon_name=request.weapon_name
    )

    return card


@router.post("/{_id}/character/make_accusation")
async def make_accusation(_id: UUID,
                          request: AccusationRequest,
                          crud: GameCRUD = Depends(GameCRUD.as_dependency),
                          user = Depends(current_active_user)):
    """
    Makes an accusation

    :param _id:
    :param character:
    :param weapon:
    :param room:
    :param crud:
    :param user:
    :return:
    """
    controller = GameDBController(game_id=_id, session=crud.session)
    character_m = controller.get_character_info(user_id=user.id)

    win = controller.make_accusation(
            current_player_id=character_m.id,
            player_name=request.character_name,
            room_name=request.room_name,
            weapon=request.weapon_name
        )

    return {"win": win}


@router.delete("/{_id}/")
async def delete_game(_id: str,
                crud: GameCRUD = Depends(GameCRUD.as_dependency),
                user = Depends(current_active_user)):
    """
    Gets the game by either the alphanumeric game key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    game = crud.get_by_id_or_key(_id=_id)

    return {
        "status": crud.delete(game.id)
    }






