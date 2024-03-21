from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
async_sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
async_engine = create_async_engine(async_sqlite_url, echo=True, connect_args=connect_args)


async def alchemy_create_db_and_tables():
    pass
    from clueless.app.db.models.user import Base
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_db_and_tables():
    from sqlalchemy.orm import relationship
    from clueless.app.db.models.room import Room
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
        yield session

