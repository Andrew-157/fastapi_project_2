from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .schemas import UserBase, RecommendationBase, FictionTypeBase, TagBase


class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    hashed_password: str

    recommendations: list["Recommendation"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "delete"}
    )


class FictionType(FictionTypeBase, table=True):
    __tablename__ = 'fiction_type'
    id: int = Field(primary_key=True, default=None)

    recommendations: list["Recommendation"] = Relationship(
        back_populates="fiction_type", sa_relationship_kwargs={"cascade": "delete"}
    )


class RecommendationTagLink(SQLModel, table=True):
    __tablename__ = 'tagged_recommendations'
    recommendation_id: int | None = Field(
        default=None, foreign_key="recommendation.id", primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )


class Recommendation(RecommendationBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    published: datetime = Field(default=datetime.utcnow())
    updated: datetime | None = Field(default=None)
    user_id: int = Field(foreign_key="user.id")
    fiction_type_id: int = Field(
        foreign_key="fiction_type.id")

    user: User = Relationship(back_populates="recommendations")
    fiction_type: FictionType = Relationship(back_populates="recommendations")
    tags: list["Tag"] = Relationship(
        back_populates="recommendations", link_model=RecommendationTagLink
    )


class Tag(TagBase, table=True):
    id: int = Field(primary_key=True, default=None)

    recommendations: list["Recommendation"] = Relationship(
        back_populates="tags", link_model=RecommendationTagLink
    )
