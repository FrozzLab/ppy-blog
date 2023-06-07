import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import desc, func

from src.backend.models import models
from src.backend.schemas import schemas


def create_user(session, new_user: models.User):
    new_user.uuid = uuid.uuid4().hex

    session.add(new_user)
    session.commit()
    session.refresh(new_user)


# def create_blog(session, new_blog_schema: schemas.BlogCreateSchema, user_id: int):
#     user_creator_model = get_user_by_id(session, user_id)
#
#     if user_creator_model is None:
#         raise HTTPException(status_code=404, detail="Blog owner does not exist")
#
#     new_blog_model = models.Blog(**new_blog_schema.dict(), created_at=datetime.utcnow())
#
#     session.add(new_blog_model)
#     session.commit()
#     session.refresh(new_blog_model)
#
#     new_user_blog_association = models.UserBlog(user_id=user_id, blog_id=new_blog_model.id)
#
#     session.add(new_user_blog_association)
#     session.commit()
#     session.refresh(new_user_blog_association)
#
#     return new_blog_model


def create_blog(session, new_blog_schema: schemas.BlogCreateSchema, user_id: int):
    user_creator_model = get_user_by_uuid(session, user_id)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Blog owner does not exist")

    new_blog_model = models.Blog(**new_blog_schema.dict(), created_at=datetime.utcnow())

    session.add(new_blog_model)
    session.commit()
    session.refresh(new_blog_model)

    return new_blog_model


def create_post(session, new_post_schema: schemas.PostCreateSchema):
    new_post_model = models.Post(**new_post_schema.dict(), created_at=datetime.utcnow())
    parent_blog_model = get_blog_by_id(session, new_post_model.blog_id)

    if parent_blog_model is None:
        raise HTTPException(status_code=404, detail="Parent blog does not exist")

    session.add(new_post_model)
    session.commit()
    session.refresh(new_post_model)

    return new_post_model


def create_comment(session, new_comment_schema: schemas.CommentCreateSchema):
    new_comment_model = models.Comment(**new_comment_schema.dict(), created_at=datetime.utcnow())
    parent_post_model = get_post_by_id(session, new_comment_model.post_id)
    user_creator_model = get_user_by_uuid(session, new_comment_model.user_id)

    if parent_post_model is None:
        raise HTTPException(status_code=404, detail="Parent post does not exist")

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Comment creator does not exist")

    session.add(new_comment_model)
    session.commit()
    session.refresh(new_comment_model)

    return new_comment_model


def create_blog_like(session, new_like_schema: schemas.BlogLikeCreateSchema):
    new_like_model = models.BlogLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    user_model = get_user_by_uuid(session, new_like_schema.user_id)
    blog_model = get_blog_by_id(session, new_like_schema.blog_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    if blog_model is None:
        raise HTTPException(status_code=404, detail="Liked blog does not exist")

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_post_like(session, new_like_schema: schemas.PostLikeCreateSchema):
    new_like_model = models.PostLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    user_model = get_user_by_uuid(session, new_like_schema.user_id)
    post_model = get_post_by_id(session, new_like_schema.post_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    if post_model is None:
        raise HTTPException(status_code=404, detail="Liked post does not exist")

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_comment_like(session, new_like_schema: schemas.CommentLikeCreateSchema):
    new_like_model = models.CommentLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    user_model = get_user_by_uuid(session, new_like_schema.user_id)
    comment_model = get_comment_by_id(session, new_like_schema.comment_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    if comment_model is None:
        raise HTTPException(status_code=404, detail="Liked comment does not exist")

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_blog_save(session, new_save_schema: schemas.BlogSaveCreateSchema):
    new_save_model = models.BlogSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    user_model = get_user_by_uuid(session, new_save_schema.user_id)
    blog_model = get_blog_by_id(session, new_save_schema.blog_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    if blog_model is None:
        raise HTTPException(status_code=404, detail="Saved blog does not exist")

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def create_post_save(session, new_save_schema: schemas.PostSaveCreateSchema):
    new_save_model = models.PostSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    user_model = get_user_by_uuid(session, new_save_schema.user_id)
    post_model = get_post_by_id(session, new_save_schema.post_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    if post_model is None:
        raise HTTPException(status_code=404, detail="Saved post does not exist")

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def create_comment_save(session, new_save_schema: schemas.CommentSaveCreateSchema):
    new_save_model = models.CommentSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    user_model = get_user_by_uuid(session, new_save_schema.user_id)
    comment_model = get_comment_by_id(session, new_save_schema.comment_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    if comment_model is None:
        raise HTTPException(status_code=404, detail="Saved comment does not exist")

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def get_user_by_uuid(session, user_uuid: str):
    return session.query(models.User).filter(models.User.uuid == user_uuid).first()


def get_user_by_name_and_password(session, user_profile_name: str, user_password: str):
    return session.query(models.User). \
        filter(models.User.profile_name == user_profile_name, models.User.password == user_password). \
        first()


def get_users_by_blog(session, blog_id: int):
    return session.query(models.User). \
        join(models.UserBlog, models.UserBlog.user_id == models.User.id). \
        filter(models.UserBlog.blog_id == blog_id). \
        all()


def get_blog_by_id(session, blog_id: int):
    return session.query(models.Blog).filter(models.Blog.id == blog_id).first()


def get_blog_by_title(session, blog_title: str):
    return session.query(models.Blog).filter(models.Blog.title == blog_title).first()


def get_post_by_id(session, post_id: int):
    return session.query(models.Post).filter(models.Post.id == post_id).first()


def get_comment_by_id(session, comment_id: int):
    return session.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_user_blogs(session, user_id: int):
    return session.query(models.Blog). \
        join(models.UserBlog, models.UserBlog.blog_id == models.Blog.id). \
        filter(models.UserBlog.user_id == user_id). \
        all()


def get_blog_posts(session, blog_id: int):
    return session.query(models.Post).filter(models.Post.blog_id == blog_id).all()


def get_post_comments(session, post_id: int):
    return session.query(models.Comment).filter(models.Comment.post_id == post_id).all()


def get_user_comments(session, user_id: int):
    return session.query(models.Comment).filter(models.Comment.user_id == user_id).all()


def get_user_followers(session, user_uuid: str):
    user = session.query(models.User).filter(models.User.uuid == user_uuid).first()
    follower_associations = user.followers if user else []
    followers = []

    for follower_association in follower_associations:
        followers.append(follower_association.follower)

    return followers


def get_user_follows(session, user_uuid: str):
    user = session.query(models.User).filter(models.User.uuid == user_uuid).first()
    follow_associations = user.follows if user else []
    follows = []

    for follow_association in follow_associations:
        follows.append(follow_association.user)

    return follows


def get_all_users(session):
    return session.query(models.User).all()


def get_all_blogs(session):
    return session.query(models.Blog).all()


def get_n_most_popular_blogs(session, amount_to_display: int):
    return session.query(models.Blog). \
        outerjoin(models.BlogLike, models.BlogLike.blog_id == models.Blog.id). \
        order_by(desc(func.count(models.BlogLike.user_id))). \
        group_by(models.Blog.id). \
        limit(amount_to_display).all()


def get_all_posts(session):
    return session.query(models.Post).all()


def get_all_comments(session):
    return session.query(models.Comment).all()


def update_user_by_uuid(session, user_update_data: schemas.UserUpdateSchema, user_uuid: str):
    given_user_model = get_user_by_uuid(session, user_uuid)

    if given_user_model is None:
        raise HTTPException(status_code=404, detail="User queued for update does not exist")

    for var, value in vars(user_update_data).items():
        setattr(given_user_model, var, value) if value else None

    session.add(given_user_model)
    session.commit()
    session.refresh(given_user_model)

    return given_user_model


def update_blog_by_id(session, blog_update_data: schemas.BlogUpdateSchema, blog_id: int):
    given_blog_model = get_blog_by_id(session, blog_id)

    if given_blog_model is None:
        raise HTTPException(status_code=404, detail="Blog queued for update does not exist")

    for var, value in vars(blog_update_data).items():
        setattr(given_blog_model, var, value) if value else None

    session.add(given_blog_model)
    session.commit()
    session.refresh(given_blog_model)

    return given_blog_model


def update_post_by_id(session, post_update_data: schemas.PostUpdateSchema, post_id: int):
    given_post_model = get_post_by_id(session, post_id)

    if given_post_model is None:
        raise HTTPException(status_code=404, detail="Post queued for update does not exist")

    for var, value in vars(post_update_data).items():
        setattr(given_post_model, var, value) if value else None

    session.add(given_post_model)
    session.commit()
    session.refresh(given_post_model)

    return given_post_model


def update_comment_by_id(session, comment_update_data: schemas.CommentUpdateSchema, comment_id: int):
    given_comment_model = get_comment_by_id(session, comment_id)

    if given_comment_model is None:
        raise HTTPException(status_code=404, detail="Comment queued for update does not exist")

    for var, value in vars(comment_update_data).items():
        setattr(given_comment_model, var, value) if value else None

    session.add(given_comment_model)
    session.commit()
    session.refresh(given_comment_model)

    return given_comment_model


def delete_user_by_id(session, user_id: int):
    session.query(models.User).filter(models.User.id == user_id).delete()
    session.commit()


def delete_blog_by_id(session, blog_id: int):
    session.query(models.Blog).filter(models.Blog.id == blog_id).delete()
    session.commit()


def delete_post_by_id(session, post_id: int):
    session.query(models.Post).filter(models.Post.id == post_id).delete()
    session.commit()


def delete_comment_by_id(session, comment_id: int):
    session.query(models.Comment).filter(models.Comment.id == comment_id).delete()
    session.commit()


def delete_blog_like_by_id(session, user_id: int, blog_id: int):
    session.query(models.BlogLike). \
        filter(models.BlogLike.user_id == user_id,
               models.BlogLike.blog_id == blog_id). \
        delete()

    session.commit()


def delete_post_like_by_id(session, user_id: int, post_id: int):
    session.query(models.PostLike). \
        filter(models.PostLike.user_id == user_id,
               models.PostLike.post_id == post_id). \
        delete()

    session.commit()


def delete_comment_like_by_id(session, user_id: int, comment_id: int):
    session.query(models.CommentLike). \
        filter(models.CommentLike.user_id == user_id,
               models.CommentLike.comment_id == comment_id). \
        delete()

    session.commit()


def delete_blog_save_by_id(session, user_id: int, blog_id: int):
    session.query(models.BlogSave). \
        filter(models.BlogSave.user_id == user_id,
               models.BlogSave.blog_id == blog_id). \
        delete()

    session.commit()


def delete_post_save_by_id(session, user_id: int, post_id: int):
    session.query(models.PostSave). \
        filter(models.PostSave.user_id == user_id,
               models.PostSave.post_id == post_id). \
        delete()

    session.commit()


def delete_comment_save_by_id(session, user_id: int, comment_id: int):
    session.query(models.CommentSave). \
        filter(models.CommentSave.user_id == user_id,
               models.CommentSave.comment_id == comment_id). \
        delete()

    session.commit()
