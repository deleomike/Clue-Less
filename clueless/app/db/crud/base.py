from abc import ABC, abstractmethod
from uuid import UUID
from sqlmodel import Session

from clueless.app.db import get_session, get_async_session, CustomSessionManager
from clueless.app.db import engine


class BaseCRUD(ABC):

    def __init__(self, session: Session, *args, **kwargs):
        self.session = session

    @classmethod
    async def as_dependency(cls):
        # # session = next(get_session())
        # session = get_async_session()
        with CustomSessionManager() as SM:
            print(SM.__dict__)
            yield cls(session=SM)

    @abstractmethod
    def get(self, _id: UUID):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass
