from src.models import models


def get_user_by_id(session, user_id: int):
    return session.query(models.User).filter(models.User.id == user_id).first()


def get_blog_by_id(session, blog_id: int):
    return session.query(models.Blog).filter(models.Blog.id == blog_id).first()


def get_post_by_id(session, post_id: int):
    return session.query(models.Post).filter(models.Post.id == post_id).first()


def get_comment_by_id(session, comment_id: int):
    return session.query(models.Comment).filter(models.Comment.id == comment_id).first()


def delete_user_by_id(session, user_id: int):
    session.query(models.User).filter(models.User.id == user_id).delete()


def delete_blog_by_id(session, blog_id: int):
    return session.query(models.Blog).filter(models.Blog.id == blog_id).delete()


def delete_post_by_id(session, post_id: int):
    return session.query(models.Post).filter(models.Post.id == post_id).delete()


def delete_comment_by_id(session, comment_id: int):
    return session.query(models.Comment).filter(models.Comment.id == comment_id).delete()
