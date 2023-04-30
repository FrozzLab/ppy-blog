from src.models import models as ml


def get_user_by_id(session, user_id: int):
    return session.query(ml.User).filter(ml.User.id == user_id).first()


def get_blog_by_id(session, blog_id: int):
    return session.query(ml.Blog).filter(ml.Blog.id == blog_id).first()


def get_post_by_id(session, post_id: int):
    return session.query(ml.Post).filter(ml.Post.id == post_id).first()


def get_comment_by_id(session, comment_id: int):
    return session.query(ml.Comment).filter(ml.Comment.id == comment_id).first()
