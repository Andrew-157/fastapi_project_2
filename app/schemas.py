from sqlmodel import SQLModel, Field
from pydantic import validator, EmailStr


class UserBase(SQLModel):
    username: str = Field(max_length=255, min_length=5,
                          unique=True, index=True)

    email: EmailStr = Field(max_length=255, unique=True,
                            index=True)
