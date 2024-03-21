from abc import ABC, abstractmethod
from uuid import UUID
from sqlmodel import Session

from clueless.app.db import get_session
from clueless.app.db import engine


class BaseCRUD(ABC):

    def __init__(self, session: Session, *args, **kwargs):
        self.session = session

    @classmethod
    def as_dependency(cls):
        yield cls(session=Session(engine))

    @abstractmethod
    def get(self, _id: UUID):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass
