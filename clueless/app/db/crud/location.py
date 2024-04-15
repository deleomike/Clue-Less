import uuid

from collections import defaultdict
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
            "Study",
            "Hall",
            "Lounge",
            "Dining Room",
            "Billiard Room",
            "Library",
            "Conservatory",
            "Ball Room",
            "Kitchen"
        ]

        names.extend(["Study-Hall Hall",
                      "Hall-Lounge Hall",
                      "Study-Library Hall",
                      "Hall-Billiard Room Hall",
                      "Lounge-Dining Room Hall",
                      "Library-Billiard Room Hall",
                      "Billiard Room-Dining Room Hall",
                      "Library-Conservatory Hall",
                      "Billiard Room-Ball Room Hall",
                      "Dining Room-Kitchen Hall",
                      "Conservatory-Ball Room Hall",
                      "Ball Room-Kitchen Hall"
                      ])
        # names.extend([f"hallway{i}" for i in range(12)])

        connections = {
            "Study":
                [
                    "Study-Hall Hall",
                    "Study-Library Hall",
                    "Kitchen",
                ],
            "Hall":
                [
                    "Study-Hall Hall",
                    "Hall-Lounge Hall",
                    "Hall-Billiard Room Hall"
                ],
            "Lounge":
                [
                    "Hall-Lounge Hall",
                    "Lounge-Dining Room Hall",
                    "Conservatory"
                ],
            "Library":
                [
                    "Library-Billiard Room Hall",
                    "Study-Library Hall",
                    "Library-Conservatory Hall",
                ],
            "Billiard Room":
                [
                    "Hall-Billiard Room Hall",
                    "Library-Billiard Room Hall",
                    "Billiard Room-Dining Room Hall",
                    "Billiard Room-Ball Room Hall"
                ],
            "Dining Room":
                [
                    "Lounge-Dining Room Hall",
                    "Billiard Room-Dining Room Hall",
                    "Dining Room-Kitchen Hall"
                ],
            "Conservatory":
                [
                    "Library-Conservatory Hall",
                    "Conservatory-Ball Room Hall",
                    "Lounge",
                ],
            "Ball Room":
                [
                    "Billiard Room-Ball Room Hall",
                    "Conservatory-Ball Room Hall",
                    "Ball Room-Kitchen Hall",
                ],
            "Kitchen":
                [
                    "Ball Room-Kitchen Hall",
                    "Dining Room-Kitchen Hall",
                    "Study"
                ]
        }

        reverse_connections = defaultdict(set)

        for name in connections:
            connects = connections[name]
            for other_name in connects:
                reverse_connections[other_name].add(name)

        locations = {}

        # Create the rooms and hallways

        for name in names:
            create = LocationCreate(game_id=game_id, name=name)
            location = self.create(location=create)
            locations[name] = location

        # Make the connections

        for name in names:
            location = locations[name]
            for reverse_connection in reverse_connections[name]:
                print(f"{reverse_connection}, {name}")
                dest = locations[reverse_connection]

                self.connect_location(location.id, dest.id)

            if "-" in name:
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

