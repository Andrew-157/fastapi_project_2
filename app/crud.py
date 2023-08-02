from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from .models import User, Recommendation, Tag, RecommendationTagLink, FictionType


def get_user_with_username(session: Session, username: str) -> User:
    return session.exec(select(User).where(User.username == username)).first()


def get_user_with_email(session: Session, email: str) -> User:
    return session.exec(select(User).where(User.email == email)).first()


def get_recommendation_by_id_with_tags_and_fiction_type(session: Session, recommendation_id: int) -> Recommendation | None:
    return session.exec(select(Recommendation).options(joinedload(Recommendation.fiction_type),
                                                       joinedload(Recommendation.tags)).
                        where(Recommendation.id == recommendation_id)).first()


def get_recommendation_by_id(session: Session, recommendation_id: int) -> Recommendation | None:
    return session.get(Recommendation, recommendation_id)


def get_fiction_type_by_slug(session: Session, fiction_type_slug: str) -> FictionType:
    return session.exec(select(FictionType).where(FictionType.slug == fiction_type_slug)).first()


def get_all_recommendations(session: Session):
    return session.exec(select(Recommendation).options(
        joinedload(Recommendation.fiction_type),
        joinedload(Recommendation.tags)).order_by(Recommendation.title)).unique().all()


def get_recommendations_by_fiction_type(session: Session, fiction_type: FictionType):
    return session.exec(select(Recommendation).options(
        joinedload(Recommendation.fiction_type),
        joinedload(Recommendation.tags)).where(Recommendation.fiction_type_id == fiction_type.id).
        order_by(Recommendation.title)).unique().all()
