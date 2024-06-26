import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.models.character import CharacterBase, Character, CharacterRead, CharacterCreate, CharacterUpdate
from clueless.app.db.models.shared import CharacterReadLinks
from clueless.app.db.models.card import CardRead, Card


class CharacterCRUD(BaseCRUD):

    def get(self, _id: UUID) -> CharacterRead:
        character = self.session.get(Character, _id)
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        return character

    def get_with_link(self, _id: UUID) -> CharacterReadLinks:
        return self.get(_id)

    def get_owned_cards(self, character_id: UUID) -> List[CardRead]:
        cards = self.session.exec(select(Card).where(Card.owner_id == character_id)).all()

        return cards

    def get_by_user_id(self, user_id: str) -> CharacterReadLinks:
        characters = self.session.exec(select(Character).where(Character.user_id==user_id)).all()
        return characters[0]

    def get_all(self) -> List[CharacterRead]:
        characters = self.session.exec(select(Character)).all()
        return characters

    def create(self, character: CharacterCreate) -> CharacterRead:

        # character.users = [str(character.host)]
        db_character = Character.model_validate(character)
        self.session.add(db_character)
        self.session.commit()
        self.session.refresh(db_character)

        return db_character

    def delete(self, _id: UUID) -> CharacterRead:
        character = self.session.get(Character, _id)
        if not character:
            raise HTTPException(status_code=404, detail="Hero not found")
        self.session.delete(character)
        self.session.commit()
        return True

    def update(self, _id: UUID, character: CharacterUpdate) -> CharacterRead:
        db_character = self.session.get(Character, _id)
        if not db_character:
            raise HTTPException(status_code=404, detail="Character not found")
        character_data = character.model_dump(exclude_unset=True)
        db_character.sqlmodel_update(character_data)
        self.session.add(db_character)
        self.session.commit()
        self.session.refresh(db_character)
        return db_character

    def change_room(self, id: UUID, location_id: UUID):
        """
        does not validate if the room is in the corresponding game

        :param id:
        :param location_id:
        :return:
        """

        character = self.get(id)

        character.location_id = location_id

        self.session.add(character)
        self.session.commit()
        self.session.refresh(character)
