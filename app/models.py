from sqlmodel import SQLModel, Field
from .schemas import UserBase


class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    hashed_password: str
