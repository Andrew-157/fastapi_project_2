from datetime import timedelta
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel import Session, select

from app.models import User, Recommendation, FictionType, Tag, Comment
from app.auth import get_password_hash

from .conftest import AuthActions


def test_get_comments(client: TestClient, session: Session):
    test_user = session.exec(select(User).where(
        User.username == 'test_user')).first()
    fiction_type = FictionType(name='movie', slug='movie')
    recommendation = Recommendation(
        title='Interstellar', short_description='Movie about space',
        opinion='My favorite movie', fiction_type=fiction_type,
        user=test_user
    )
    comment_1 = Comment(content='I agree', user=test_user,
                        recommendation=recommendation)
    comment_2 = Comment(content='I agree 2', user=test_user,
                        recommendation=recommendation)
    comment_2.published = comment_2.published + timedelta(minutes=15)
    session.add(comment_1)
    session.add(comment_2)
    session.commit()
    response = client.get(f'/recommendations/{recommendation.id}/comments')
    assert response.status_code == status.HTTP_200_OK
    comments_for_recommendation = session.exec(select(Comment).
                                               where(Comment.recommendation_id == recommendation.id)).all()
    assert len(response.json()) == len(comments_for_recommendation)
    assert response.json()[0]['id'] == comment_1.id
    response = client.get(
        f'/recommendations/{recommendation.id}/comments?by_published_date_descending=false'
    )
    assert len(response.json()) == len(comments_for_recommendation)
    assert response.json()[0]['id'] == comment_1.id
    response = client.get(
        f'/recommendations/{recommendation.id}/comments?by_published_date_descending=true'
    )
    assert len(response.json()) == len(comments_for_recommendation)
    assert response.json()[0]['id'] == comment_2.id
    response = client.get(
        f'/recommendations/{recommendation.id}/comments?offset=1'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == comment_2.id
    response = client.get(
        f'/recommendations/{recommendation.id}/comments?limit=1'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == comment_1.id


def test_get_comments_for_nonexistent_recommendation(client: TestClient, session: Session):
    nonexistent_recommendation_id = 89
    response = client.get(
        f'/recommendations/{nonexistent_recommendation_id}/comments')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'detail' in response.json()
    error_detail = f"Recommendation with id {nonexistent_recommendation_id} was not found"
    assert response.json()['detail'] == error_detail


def test_post_comment_for_not_logged_user(client: TestClient):
    response = client.post('/recommendations/78/comments')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "www-authenticate" in dict(response.headers)
    assert dict(response.headers)['www-authenticate'] == 'Bearer'


def test_post_comment_for_nonexistent_recommendation(client: TestClient, auth: AuthActions):
    token = auth.login_user_for_token()
    headers = {'Authorization': f'Bearer {token}'}
    nonexistent_recommendation_id = 49
    response = client.post(f'/recommendations/{nonexistent_recommendation_id}/comments',
                           json={'content': 'comment'}, headers=headers)
    print(response.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'detail' in response.json()
    error_detail = f"Recommendation with id {nonexistent_recommendation_id} was not found"
    assert response.json()['detail'] == error_detail


def test_logged_user_posts_comment(client: TestClient, auth: AuthActions, session: Session):
    test_user = session.exec(select(User).where(
        User.username == 'test_user')).first()
    fiction_type = FictionType(name='movie', slug='movie')
    recommendation = Recommendation(
        title='Interstellar', short_description='Movie about space',
        opinion='My favorite movie', fiction_type=fiction_type,
        user=test_user
    )
