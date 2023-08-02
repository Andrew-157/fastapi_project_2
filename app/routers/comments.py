from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Path, HTTPException, status, Depends
from sqlmodel import Session

from ..auth import get_current_user
from ..crud import get_recommendation_by_id, get_comment_by_id_and_recommendation_id
from ..schemas import CommentRead, CommentCreate, CommentUpdate
from ..models import Comment, User
from ..database import get_session


router = APIRouter(
    tags=['comments']
)


@router.post('/recommendations/{recommendation_id}/comment',
             response_model=CommentRead,
             status_code=status.HTTP_201_CREATED)
async def post_comment(
    recommendation_id: Annotated[int, Path()],
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    data: Annotated[CommentCreate, Body()]
):
    recommendation = get_recommendation_by_id(
        session=session, recommendation_id=recommendation_id
    )
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with id {recommendation_id}\
                was not found"
        )
    new_comment = Comment(
        content=data.content,
        recommendation_id=recommendation.id,
        user_id=current_user.id
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment


@router.get('/recommendations/{recommendation_id}/comments/{comment_id}',
            response_model=CommentRead)
async def get_comment(recommendation_id: Annotated[int, Path()],
                      comment_id: Annotated[int, Path()],
                      session: Annotated[Session, Depends(get_session)]):
    recommendation = get_recommendation_by_id(session=session,
                                              recommendation_id=recommendation_id)
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with id {recommendation_id } was not found"
        )
    comment = get_comment_by_id_and_recommendation_id(
        session=session,
        recommendation_id=recommendation_id,
        comment_id=comment_id
    )
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} for recommendation with id {recommendation_id} was not found"
        )
    return comment


@router.put('/recommendations/{recommendation_id}/comments/{comment_id}',
            response_model=CommentRead)
async def update_comment(recommendation_id: Annotated[int, Path()],
                         comment_id: Annotated[int, Path()],
                         session: Annotated[Session, Depends(get_session)],
                         data: Annotated[CommentUpdate, Body()],
                         current_user: Annotated[User, Depends(get_current_user)]):
    recommendation = get_recommendation_by_id(session=session,
                                              recommendation_id=recommendation_id)
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} for recommendation with id {recommendation_id} was not found"
        )
    comment = get_comment_by_id_and_recommendation_id(
        session=session,
        recommendation_id=recommendation_id,
        comment_id=comment_id
    )
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id}\
                for recommendation with id {recommendation_id}\
                was not found"
        )
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User has no permission to update comment with id {comment_id}"
        )
    data: dict = data.dict()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Body provided"
        )
    new_content = data.get('content')
    if new_content:
        comment.content = new_content
    comment.updated = datetime.utcnow()
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.delete('/recommendations/{recommendation_id}/comments/{comment_id}',
               status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_comment(
    recommendation_id: Annotated[int, Path()],
    comment_id: Annotated[int, Path()],
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    recommendation = get_recommendation_by_id(session=session,
                                              recommendation_id=recommendation_id)
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} for recommendation with id {recommendation_id} was not found"
        )
    comment = get_comment_by_id_and_recommendation_id(
        session=session,
        recommendation_id=recommendation_id,
        comment_id=comment_id
    )
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} for recommendation with id {recommendation_id} was not found"
        )
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User has no permission to update comment with id {comment_id}"
        )
    session.delete(comment)
    session.commit()
    return None
