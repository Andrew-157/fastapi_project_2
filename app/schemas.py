import re
from datetime import datetime
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


class RecommendationCreate(RecommendationBase):
    fiction_type: str = Field(min_length=4,
                              max_length=255,
                              unique=True)
    tags: list[str] = Field(min_items=1)


class FictionTypeBase(SQLModel):
    name: str = Field(min_length=4,
                      max_length=255,
                      unique=True)
    slug: str = Field(min_length=4, max_length=300,
                      unique=True)


class FictionTypeRead(FictionTypeBase):
    id: int


class TagBase(SQLModel):
    name: str = Field(unique=True, max_length=255,
                      min_length=4)


class TagRead(TagBase):
    id: int


class CommentBase(SQLModel):
    content: str


class RecommendationRead(RecommendationBase):
    id: int
    user_id: int
    published: datetime
    updated: datetime | None
    fiction_type: FictionTypeRead
    tags: list[TagRead]


class RecommendationUpdate(SQLModel):
    title: str | None = Field(max_length=255, default=None)
    short_description: str | None = Field(default=None)
    opinion: str | None = Field(default=None)
    fiction_type: str | None = Field(min_length=4,
                                     max_length=255,
                                     default=None)
    tags: list[str] | None = Field(min_items=1,
                                   default=None)


class CommentRead(CommentBase):
    id: int
    user_id: int
    recommendation_id: int
    published: datetime
    updated: datetime | None


class CommentCreate(CommentBase):
    pass


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
