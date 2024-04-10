import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.models.location import LocationBase, Location, LocationRead, LocationCreate, LocationUpdate
from clueless.app.db.models.shared import LocationReadLinks


class LocationCRUD(BaseCRUD):

    def get(self, _id: UUID) -> LocationReadLinks:
        location = self.session.get(Location, _id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location

    def get_all(self) -> List[LocationRead]:
        locations = self.session.exec(select(Location)).all()
        return locations

    def create_all_game_rooms(self, game_id):
        names = [
            "study",
            "hall",
            "lounge",
            "dining_room",
            "billiard_room",
            "library",
            "conservatory",
            "ball_room",
            "kitchen"
        ]

        names.extend([f"hallway{i}" for i in range(12)])

        connections = {
            "study":
                [
                    "hallway0",
                    "hallway2",
                    "kitchen",
                ],
            "hall":
                [
                    "hallway0",
                    "hallway1",
                    "hallway3"
                ],
            "lounge":
                [
                    "hallway1",
                    "hallway4",
                    "conservatory"
                ],
            "library":
                [
                    "hallway5",
                    "hallway2",
                    "hallway7",
                ],
            "billiard_room":
                [
                    "hallway3",
                    "hallway5",
                    "hallway6",
                    "hallway8"
                ],
            "dining_room":
                [
                    "hallway4",
                    "hallway6",
                    "hallway9"
                ],
            "conservatory":
                [
                    "hallway7",
                    "hallway10",
                    "lounge",
                ],
            "ball_room":
                [
                    "hallway8",
                    "hallway10",
                    "hallway11",
                ],
            "kitchen":
                [
                    "hallway11",
                    "hallway9",
                    "study"
                ]
        }

        locations = {}

        # Create the rooms and hallways

        for name in names:
            create = LocationCreate(game_id=game_id, name=name)
            location = self.create(location=create)
            locations[name] = location

        # Make the connections

        for name in names:
            location = locations[name]
            if "hallway" in name:
                continue
            for connection in connections[name]:
                dest = locations[connection]

                self.connect_location(location.id, dest.id)

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

    def connect_location(self, _id: UUID, dest: UUID):
        origin = self.get(_id)
        destination = self.get(dest)

        origin.connected_locations.append(destination)
        self.session.add(origin)
        self.session.commit()

