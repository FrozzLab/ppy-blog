from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from src.backend.models.models import User, Blog, Post, Comment, BlogLike, PostLike, CommentLike, BlogSave, PostSave, \
    CommentSave
from src.backend.schemas.create_schemas import UserCreateSchema, BlogCreateSchema, PostCreateSchema, \
    CommentCreateSchema, BlogLikeCreateSchema, PostLikeCreateSchema, CommentLikeCreateSchema, BlogSaveCreateSchema, \
    PostSaveCreateSchema, CommentSaveCreateSchema
from src.backend.services.get import get_user_by_username, get_user_by_id, get_blog_by_title, get_blog_by_id, \
    get_user_blogs_by_id, get_post_by_title, get_post_by_id, get_blog_like_by_id, get_post_like_by_id, \
    get_comment_by_id, get_comment_like_by_id, get_blog_save_by_id, get_post_save_by_id, get_comment_save_by_id


def create_user(session: Session, new_user_schema: UserCreateSchema) -> User:
    existing_user_model = get_user_by_username(session, new_user_schema.profile_name)

    if existing_user_model is not None:
        raise HTTPException(status_code=400, detail="User with given profile name already exists")

    new_user_model = User(**new_user_schema.dict(), created_at=datetime.utcnow())
    new_user_model.uuid = uuid4()

    session.add(new_user_model)
    session.commit()
    session.refresh(new_user_model)

    return new_user_model


def create_blog(session: Session, new_blog_schema: BlogCreateSchema) -> Blog:
    user_creator_model = get_user_by_id(session, new_blog_schema.user_id)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Blog creator does not exist")

    existing_blog_model = get_blog_by_title(session, new_blog_schema.title)

    if existing_blog_model is not None:
        raise HTTPException(status_code=400, detail="Blog with given title already exists")

    new_blog_dict = new_blog_schema.dict()
    del new_blog_dict["user_id"]

    new_blog_model = Blog(**new_blog_dict, created_at=datetime.utcnow())
    new_blog_model.uuid = uuid4()
    new_blog_model.owners.append(user_creator_model)

    session.add(new_blog_model)
    session.commit()
    session.refresh(new_blog_model)

    return new_blog_model


def create_post(session: Session, new_post_schema: PostCreateSchema) -> Post:
    parent_blog_model = get_blog_by_id(session, new_post_schema.blog_id)

    if parent_blog_model is None:
        raise HTTPException(status_code=404, detail="Parent blog does not exist")

    user_creator_model = get_user_by_id(session, new_post_schema.user_id)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Post creator does not exist")

    creator_blogs = get_user_blogs_by_id(session, user_creator_model.id)

    if parent_blog_model not in creator_blogs:
        raise HTTPException(status_code=400, detail="User does not own blog")

    existing_post_model = get_post_by_title(session, new_post_schema.title, new_post_schema.blog_id)

    if existing_post_model is not None:
        raise HTTPException(status_code=400, detail="Post with given title already exists in given blog")

    new_post_model = Post(**new_post_schema.dict(), created_at=datetime.utcnow())
    new_post_model.uuid = uuid4()
    new_post_model.user = user_creator_model
    new_post_model.blog = parent_blog_model

    session.add(new_post_model)
    session.commit()
    session.refresh(new_post_model)

    return new_post_model


def create_comment(session: Session, new_comment_schema: CommentCreateSchema) -> Comment:
    parent_post_model = get_post_by_id(session, new_comment_schema.post_id)

    if parent_post_model is None:
        raise HTTPException(status_code=404, detail="Parent post does not exist")

    user_creator_model = get_user_by_id(session, new_comment_schema.user_id)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Comment creator does not exist")

    new_comment_model = Comment(**new_comment_schema.dict(), created_at=datetime.utcnow())
    new_comment_model.uuid = uuid4()
    new_comment_model.user = user_creator_model
    new_comment_model.post = parent_post_model

    session.add(new_comment_model)
    session.commit()
    session.refresh(new_comment_model)

    return new_comment_model


def create_blog_like(session: Session, new_like_schema: BlogLikeCreateSchema) -> BlogLike:
    liking_user_model = get_user_by_id(session, new_like_schema.user_id)

    if liking_user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    liked_blog_model = get_blog_by_id(session, new_like_schema.blog_id)

    if liked_blog_model is None:
        raise HTTPException(status_code=404, detail="Liked blog does not exist")

    existing_blog_like_model = get_blog_like_by_id(session, new_like_schema.user_id, new_like_schema.blog_id)

    if existing_blog_like_model is not None:
        raise HTTPException(status_code=400, detail="Blog has already been liked")

    new_like_model = BlogLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    new_like_model.user = liking_user_model
    new_like_model.blog = liked_blog_model

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_post_like(session: Session, new_like_schema: PostLikeCreateSchema) -> PostLike:
    liking_user_model = get_user_by_id(session, new_like_schema.user_id)

    if liking_user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    liked_post_model = get_post_by_id(session, new_like_schema.post_id)

    if liked_post_model is None:
        raise HTTPException(status_code=404, detail="Liked post does not exist")

    existing_post_like_model = get_post_like_by_id(session, new_like_schema.user_id, new_like_schema.post_id)

    if existing_post_like_model is not None:
        raise HTTPException(status_code=400, detail="Post has already been liked")

    new_like_model = PostLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    new_like_model.user = liking_user_model
    new_like_model.post = liked_post_model

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_comment_like(session: Session, new_like_schema: CommentLikeCreateSchema) -> CommentLike:
    liking_user_model = get_user_by_id(session, new_like_schema.user_id)

    if liking_user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    liked_comment_model = get_comment_by_id(session, new_like_schema.comment_id)

    if liked_comment_model is None:
        raise HTTPException(status_code=404, detail="Liked comment does not exist")

    existing_comment_like_model = get_comment_like_by_id(session, new_like_schema.user_id, new_like_schema.comment_id)

    if existing_comment_like_model is not None:
        raise HTTPException(status_code=400, detail="Comment has already been liked")

    new_like_model = CommentLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    new_like_model.user = liking_user_model
    new_like_model.comment = liked_comment_model

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_blog_save(session: Session, new_save_schema: BlogSaveCreateSchema) -> BlogSave:
    saving_user_model = get_user_by_id(session, new_save_schema.user_id)

    if saving_user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    saving_blog_model = get_blog_by_id(session, new_save_schema.blog_id)

    if saving_blog_model is None:
        raise HTTPException(status_code=404, detail="Saved blog does not exist")

    existing_blog_save_model = get_blog_save_by_id(session, new_save_schema.user_id, new_save_schema.blog_id)

    if existing_blog_save_model is not None:
        raise HTTPException(status_code=400, detail="Blog has already been saved")

    new_save_model = BlogSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    new_save_model.user = saving_user_model
    new_save_model.blog = saving_blog_model

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def create_post_save(session: Session, new_save_schema: PostSaveCreateSchema) -> PostSave:
    saving_user_model = get_user_by_id(session, new_save_schema.user_id)

    if saving_user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    saved_post_model = get_post_by_id(session, new_save_schema.post_id)

    if saved_post_model is None:
        raise HTTPException(status_code=404, detail="Saved post does not exist")

    existing_post_save_model = get_post_save_by_id(session, new_save_schema.user_id, new_save_schema.post_id)

    if existing_post_save_model is not None:
        raise HTTPException(status_code=400, detail="Post has already been saved")

    new_save_model = PostSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    new_save_model.user = saving_user_model
    new_save_model.post = saved_post_model

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def create_comment_save(session: Session, new_save_schema: CommentSaveCreateSchema) -> CommentSave:
    saving_user_model = get_user_by_id(session, new_save_schema.user_id)

    if saving_user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    saved_comment_model = get_comment_by_id(session, new_save_schema.comment_id)

    if saved_comment_model is None:
        raise HTTPException(status_code=404, detail="Saved comment does not exist")

    existing_comment_save_model = get_comment_save_by_id(session, new_save_schema.user_id, new_save_schema.comment_id)

    if existing_comment_save_model is not None:
        raise HTTPException(status_code=400, detail="Comment has already been saved")

    new_save_model = CommentSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    new_save_model.user = saving_user_model
    new_save_model.comment = saved_comment_model

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model
