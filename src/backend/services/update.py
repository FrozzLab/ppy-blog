from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.models.models import User, Blog, Post, Comment
from src.backend.schemas.update_schemas import UserUpdateSchema, BlogUpdateSchema, PostUpdateSchema, CommentUpdateSchema
from src.backend.services.get import get_user_by_uuid, get_blog_by_uuid, get_post_by_uuid, get_comment_by_uuid


def update_user_by_uuid(session: Session, user_update_data: UserUpdateSchema, user_uuid: UUID) -> Type[User]:
    given_user_model = get_user_by_uuid(session, user_uuid)

    if given_user_model is None:
        raise HTTPException(status_code=404, detail="User queued for update does not exist")

    for var, value in vars(user_update_data).items():
        setattr(given_user_model, var, value) if value else None

    session.add(given_user_model)
    session.commit()
    session.refresh(given_user_model)

    return given_user_model


def update_blog_by_uuid(session: Session, blog_update_data: BlogUpdateSchema, blog_uuid: UUID) -> Type[Blog]:
    given_blog_model = get_blog_by_uuid(session, blog_uuid)

    if given_blog_model is None:
        raise HTTPException(status_code=404, detail="Blog queued for update does not exist")

    for var, value in vars(blog_update_data).items():
        setattr(given_blog_model, var, value) if value else None

    session.add(given_blog_model)
    session.commit()
    session.refresh(given_blog_model)

    return given_blog_model


def update_post_by_uuid(session: Session, post_update_data: PostUpdateSchema, post_uuid: UUID) -> Type[Post]:
    given_post_model = get_post_by_uuid(session, post_uuid)

    if given_post_model is None:
        raise HTTPException(status_code=404, detail="Post queued for update does not exist")

    for var, value in vars(post_update_data).items():
        setattr(given_post_model, var, value) if value else None

    session.add(given_post_model)
    session.commit()
    session.refresh(given_post_model)

    return given_post_model


def update_comment_by_uuid(session: Session,
                           comment_update_data: CommentUpdateSchema,
                           comment_uuid: UUID) -> Type[Comment]:
    given_comment_model = get_comment_by_uuid(session, comment_uuid)

    if given_comment_model is None:
        raise HTTPException(status_code=404, detail="Comment queued for update does not exist")

    for var, value in vars(comment_update_data).items():
        setattr(given_comment_model, var, value) if value else None

    session.add(given_comment_model)
    session.commit()
    session.refresh(given_comment_model)

    return given_comment_model
