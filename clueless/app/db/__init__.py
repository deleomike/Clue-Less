from typing import AsyncGenerator

from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
async_sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(
    sqlite_url,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True,
    # pool_size=30,
    # max_overflow=120
)
async_engine = create_async_engine(async_sqlite_url, echo=False, connect_args=connect_args)

async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except:
            session.rollback()
        finally:
            print("----Closing ASYNC Session-----")
            session.close()


async def alchemy_create_db_and_tables():
    pass
    from clueless.app.db.models.user import Base
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_db_and_tables():
    from sqlalchemy.orm import relationship
    from clueless.app.db.models.game import Game
    from clueless.app.db.models.room import Room
    from clueless.app.db.models.location import Location
    from clueless.app.db.models.character import Character
    from clueless.app.db.models.card import Card
    from clueless.app.db.models.CardCharacterLink import CardCharacterLink
    # from clueless.app.db.models.user import User, UserDB
    from clueless.app.db.models.user import User, Base
    #
    # SQLModel.metadata = Base.metadata
    #
    # print(Base.metadata)

    # # Update the User SQLAlchemy table after Room class definition
    # User.room = relationship("Room", back_populates="users")
    #
    # # print(Room.__dict__)

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        except:
            session.rollback()
        finally:
            print("----Closing session----")
            session.close()


class CustomSessionManager:
    def __init__(self):
        self.session = Session(engine)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @classmethod
    def as_yield(cls):
        yield cls()
