import re
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, Field
from pydantic import validator

from ..auth import create_access_token, get_current_user, authenticate_user, get_password_hash, Token,\
    ACCESS_TOKEN_EXPIRE_HOURS
from ..database import get_session
from ..schemas import UserCreate, UserRead, UserBase
from ..models import User
from ..crud import get_user_with_username, get_user_with_email


router = APIRouter(
    tags=['users'],
    prefix='/auth'
)


@router.post("/register", response_model=UserRead)
async def register(*, session: Annotated[Session, Depends(get_session)],
                   user: Annotated[UserCreate, Body()]):
    if get_user_with_username(session=session, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Duplicate username"
        )
    if get_user_with_email(session=session, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Duplicate email"
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username,
                    email=user.email,
                    hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    user = authenticate_user(session=session,
                             username=form_data.username,
                             password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token,
            "token_type": "bearer"}


@router.get("/users/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


class UserUpdate(SQLModel):
    username: str | None = Field(default=None, min_length=5, max_length=255)
    email: str | None = Field(default=None, min_length=5, max_length=255)

    @validator("email")
    def email_valid(cls, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError("Not valid email")
        return value


@router.patch("/users/me/update", response_model=UserRead)
async def update_credentials(
        user_credentials: Annotated[UserUpdate, Body()],
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)):
    user_credentials: dict = user_credentials.dict(exclude_unset=True)
    if not user_credentials:
        return current_user
    else:
        new_username = user_credentials.get('username')
        if new_username:
            user_with_username = get_user_with_username(
                session=session, username=new_username)
            if user_with_username and (user_with_username != current_user):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Duplicate username")
            current_user.username = new_username
        new_email = user_credentials.get('email')
        if new_email:
            user_with_email = get_user_with_email(
                session=session, email=new_email)
            if user_with_email and (user_with_email != current_user):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Duplicate email")
            current_user.email = new_email
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user
