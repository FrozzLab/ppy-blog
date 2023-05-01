from datetime import datetime

from fastapi import HTTPException

from src.models import models
from src.schemas import schemas


def create_user(session, new_user: models.User):
    session.add(new_user)
    session.commit()
    session.refresh(new_user)


def create_blog(session, new_blog_schema: schemas.BlogCreateSchema, user_id: int):
    user_creator_model = get_user_by_id(session)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Blog owner does not exist")

    new_blog_model = models.Blog(**new_blog_schema.dict(), created_at=datetime.utcnow())

    session.add(new_blog_model)
    session.commit()
    session.refresh(new_blog_model)

    new_user_blog_association = models.UserBlog(user_id=user_id, blog_id=new_blog_model.id)

    session.add(new_user_blog_association)
    session.commit()
    session.refresh(new_user_blog_association)

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
    user_creator_model = get_user_by_id(session, new_comment_model.user_id)

    if parent_post_model is None:
        raise HTTPException(status_code=404, detail="Parent post does not exist")

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Comment creator does not exist")

    session.add(new_comment_model)
    session.commit()
    session.refresh(new_comment_model)

    return new_comment_model


def get_user_by_id(session, user_id: int):
    return session.query(models.User).filter(models.User.id == user_id).first()


def get_blog_by_id(session, blog_id: int):
    return session.query(models.Blog).filter(models.Blog.id == blog_id).first()


def get_post_by_id(session, post_id: int):
    return session.query(models.Post).filter(models.Post.id == post_id).first()


def get_comment_by_id(session, comment_id: int):
    return session.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_user_blogs(session, user_id):
    return session.query(models.Blog).\
                   join(models.UserBlog, models.UserBlog.blog_id == models.Blog.id).\
                   filter(models.UserBlog.user_id == user_id).\
                   all()


def get_blog_posts(session, blog_id):
    return session.query(models.Post).filter(models.Post.blog_id == blog_id).all()


def get_post_comments(session, post_id):
    return session.query(models.Comment).filter(models.Comment.post_id == post_id).all()


def get_user_comments(session, user_id):
    return session.query(models.Comment).filter(models.Comment.user_id == user_id).all()


def get_user_followers(session, user_id):
    return session.query(models.User).\
                   join(models.UserFollowing, models.UserFollowing.follower_id == models.User.id).\
                   filter(models.UserFollowing.user_id == user_id).\
                   all()


def get_user_follows(session, user_id):
    return session.query(models.User).\
                   join(models.UserFollowing, models.UserFollowing.user_id == models.User.id).\
                   filter(models.UserFollowing.follower_id == user_id).\
                   all()


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
