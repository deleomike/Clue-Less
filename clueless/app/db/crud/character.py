import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.models.location import LocationBase, Location, LocationRead, LocationCreate, LocationUpdate


class LocationCRUD(BaseCRUD):

    def get(self, _id: UUID) -> LocationRead:
        location = self.session.get(Location, _id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location

    def get_all(self) -> List[LocationRead]:
        locations = self.session.exec(select(Location)).all()
        return locations

    def create(self, location: LocationCreate) -> LocationRead:

        # location.users = [str(location.host)]
        db_location = Location.model_validate(location)
        self.session.add(db_location)
        self.session.commit()
        self.session.refresh(db_location)

        return db_location

    def delete(self, _id: UUID) -> LocationRead:
        location = self.session.get(Location, _id)
        if not location:
            raise HTTPException(status_code=404, detail="Hero not found")
        self.session.delete(location)
        self.session.commit()
        return True

    def update(self, _id: UUID, location: LocationUpdate) -> LocationRead:
        db_location = self.session.get(Location, _id)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location not found")
        location_data = location.model_dump(exclude_unset=True)
        db_location.sqlmodel_update(location_data)
        self.session.add(db_location)
        self.session.commit()
        self.session.refresh(db_location)
        return db_location

