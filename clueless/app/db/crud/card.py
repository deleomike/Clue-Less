import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.models.card import CardBase, Card, CardRead, CardCreate, CardUpdate


class CardCRUD(BaseCRUD):

    def get(self, _id: UUID) -> CardRead:
        card = self.session.get(Card, _id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        return card

    def get_all(self) -> List[CardRead]:
        cards = self.session.exec(select(Card)).all()
        return cards

    def create(self, card: CardCreate) -> CardRead:

        # card.users = [str(card.host)]
        db_card = Card.model_validate(card)
        self.session.add(db_card)
        self.session.commit()
        self.session.refresh(db_card)

        return db_card

    def delete(self, _id: UUID) -> CardRead:
        card = self.session.get(Card, _id)
        if not card:
            raise HTTPException(status_code=404, detail="Hero not found")
        self.session.delete(card)
        self.session.commit()
        return True

    def update(self, _id: UUID, card: CardUpdate) -> CardRead:
        db_card = self.session.get(Card, _id)
        if not db_card:
            raise HTTPException(status_code=404, detail="Card not found")
        card_data = card.model_dump(exclude_unset=True)
        db_card.sqlmodel_update(card_data)
        self.session.add(db_card)
        self.session.commit()
        self.session.refresh(db_card)
        return db_card

