from sqlmodel import SQLModel, Field


class UserBase(SQLModel):

    username: Optional[str] = Field(index=True)
    password: Optional[str] = Field(index=False)