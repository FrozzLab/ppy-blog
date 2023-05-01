from src.models import models


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


def delete_blog_by_id(session, blog_id: int):
    return session.query(models.Blog).filter(models.Blog.id == blog_id).delete()


def delete_post_by_id(session, post_id: int):
    return session.query(models.Post).filter(models.Post.id == post_id).delete()


def delete_comment_by_id(session, comment_id: int):
    return session.query(models.Comment).filter(models.Comment.id == comment_id).delete()
