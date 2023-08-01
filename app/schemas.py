import re
from sqlmodel import SQLModel, Field
from pydantic import validator


class UserBase(SQLModel):
    username: str = Field(max_length=255, min_length=5,
                          unique=True, index=True)

    email: str = Field(max_length=255, unique=True,
                       index=True)

    @validator("email")
    def email_valid(cls, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError("Not valid email address")
        return value


class RecommendationBase(SQLModel):
    title: str = Field(max_length=255)
    short_description: str
    opinion: str


class FictionTypeBase(SQLModel):
    name: str = Field(min_length=4,
                      max_length=255,
                      unique=True)


class TagBase(SQLModel):
    name: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: str = Field(max_length=255, min_length=5,
                          default=None)
    email: str = Field(max_length=255, default=None)

    @validator("email")
    def email_valid(cls, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError("Not valid email address")
        return value
