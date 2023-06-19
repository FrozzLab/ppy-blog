from typing import Type

from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.models.models import User, Blog, Post, Comment, BlogLike, PostLike, CommentLike, BlogSave, PostSave, \
    CommentSave


def get_user_by_id(session: Session, user_id: int) -> Type[User] | None:
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_uuid(session: Session, user_uuid: UUID) -> Type[User] | None:
    return session.query(User).filter(User.uuid == user_uuid).first()


def get_user_by_username(session: Session, user_profile_name: str) -> Type[User] | None:
    return session.query(User).filter(User.profile_name == user_profile_name).first()


def get_user_by_username_and_password(session: Session,
                                      user_profile_name: str,
                                      user_password: str) -> Type[User] | None:
    return session.query(User). \
        filter(User.profile_name == user_profile_name
               and User.password == user_password). \
        first()


def get_users_by_blog(session: Session, blog_uuid: UUID) -> list[Type[User]]:
    return session.query(Blog).filter(Blog.uuid == blog_uuid).first().owners


def get_blog_by_id(session: Session, blog_id: int) -> Type[Blog] | None:
    return session.query(Blog).filter(Blog.id == blog_id).first()


def get_blog_by_uuid(session: Session, blog_uuid: UUID) -> Type[Blog] | None:
    return session.query(Blog).filter(Blog.uuid == blog_uuid).first()


def get_blog_by_title(session: Session, blog_title: str) -> Type[Blog] | None:
    return session.query(Blog).filter(Blog.title == blog_title).first()


def get_post_by_id(session: Session, post_id: int) -> Type[Post] | None:
    return session.query(Post).filter(Post.id == post_id).first()


def get_post_by_uuid(session: Session, post_uuid: UUID) -> Type[Post] | None:
    return session.query(Post).filter(Post.uuid == post_uuid).first()


# Requires a relevant blog ID to be passed as the website allows for
# posts with the same name to appear across multiple blogs
def get_post_by_title(session: Session, post_title: str, blog_id: int) -> Type[Post] | None:
    return session.query(Post).filter(Post.title == post_title and Post.blog.id == blog_id).first()


def get_comment_by_id(session: Session, comment_id: int) -> Type[Comment] | None:
    return session.query(Comment).filter(Comment.id == comment_id).first()


def get_comment_by_uuid(session: Session, comment_uuid: UUID) -> Type[Comment] | None:
    return session.query(Comment).filter(Comment.uuid == comment_uuid).first()


def get_user_blogs_by_id(session: Session, user_id: int) -> list[Type[Blog]]:
    return session.query(User).filter(User.id == user_id).first().blogs


def get_user_blogs_by_uuid(session: Session, user_uuid: UUID) -> list[Type[Blog]]:
    return session.query(User).filter(User.uuid == user_uuid).first().blogs


def get_blog_posts_by_id(session: Session, blog_id: int) -> list[Type[Post]]:
    return session.query(Blog).filter(Blog.id == blog_id).first().posts


def get_blog_posts_by_uuid(session: Session, blog_uuid: UUID) -> list[Type[Post]]:
    return session.query(Blog).filter(Blog.uuid == blog_uuid).first().posts


def get_post_comments_by_id(session: Session, post_id: int) -> list[Type[Comment]]:
    return session.query(Post).filter(Post.id == post_id).first().comments


def get_post_comments_by_uuid(session: Session, post_uuid: UUID) -> list[Type[Comment]]:
    return session.query(Post).filter(Post.uuid == post_uuid).first().comments


def get_user_comments_by_id(session: Session, user_id: int) -> list[Type[Comment]]:
    return session.query(User).filter(User.id == user_id).first().comments


def get_user_comments_by_uuid(session: Session, user_uuid: UUID) -> list[Type[Comment]]:
    return session.query(User).filter(User.id == user_uuid).first().comments


def get_user_followers_by_uuid(session: Session, user_uuid: UUID) -> list[Type[User]]:
    follower_associations = session.query(User).filter(User.uuid == user_uuid).first().follower_associations
    return [follower_association.follower for follower_association in follower_associations]


def get_user_follows_by_uuid(session: Session, user_uuid: UUID) -> list[Type[User]]:
    follow_associations = session.query(User).filter(User.uuid == user_uuid).first().follow_associations
    return [follow_association.user for follow_association in follow_associations]


def get_all_users(session: Session) -> list[Type[User]]:
    return session.query(User).all()


def get_all_blogs(session: Session) -> list[Type[Blog]]:
    return session.query(Blog).all()


# Tried to adapt it using the blog_like_associations field in Blog, but doing so
# resulted in errors that I couldn't solve, so until I figure it out it will have
# to stay this way
# TODO: Fix get_n_most_popular_blogs to use blog_like_associations
def get_n_most_popular_blogs(session: Session, amount_to_display: int) -> list[Type[Blog]]:
    return session.query(Blog). \
        outerjoin(BlogLike, BlogLike.blog_id == Blog.id). \
        order_by(desc(func.count(BlogLike.user_id))). \
        group_by(Blog.id). \
        limit(amount_to_display).all()


def get_all_posts(session: Session) -> list[Type[Post]]:
    return session.query(Post).all()


def get_all_comments(session: Session) -> list[Type[Comment]]:
    return session.query(Comment).all()


def get_blog_like_by_id(session: Session, user_id: int, blog_id: int) -> Type[BlogLike] | None:
    return session.query(BlogLike).filter(BlogLike.user_id == user_id and BlogLike.blog_id == blog_id).first()


def get_blog_like_count_by_uuid(session: Session, blog_uuid: UUID) -> int | None:
    return session.query(Blog).filter(Blog.uuid == blog_uuid).first().blog_like_associations.len()


def get_blog_save_by_id(session: Session, user_id: int, blog_id: int) -> Type[BlogSave] | None:
    return session.query(BlogSave).filter(BlogSave.user_id == user_id and BlogSave.blog_id == blog_id).first()


def get_blog_save_count_by_uuid(session: Session, blog_uuid: UUID) -> int | None:
    return session.query(Blog).filter(Blog.uuid == blog_uuid).first().blog_save_associations.len()


def get_post_like_by_id(session: Session, user_id: int, post_id: int) -> Type[PostLike] | None:
    return session.query(PostLike).filter(PostLike.user_id == user_id and PostLike.post_id == post_id).first()


def get_post_like_count_by_uuid(session: Session, post_uuid: UUID) -> int | None:
    return session.query(Post).filter(Post.uuid == post_uuid).first().post_like_associations.len()


def get_post_save_by_id(session: Session, user_id: int, post_id: int) -> Type[PostSave] | None:
    return session.query(PostSave).filter(PostSave.user_id == user_id and PostSave.post_id == post_id).first()


def get_post_save_count_by_uuid(session: Session, post_uuid: UUID) -> int | None:
    return session.query(Post).filter(Post.uuid == post_uuid).first().post_save_associations.len()


def get_comment_like_by_id(session: Session, user_id: int, comment_id: int) -> Type[CommentLike] | None:
    return session.query(CommentLike). \
        filter(CommentLike.user_id == user_id
               and CommentLike.comment_id == comment_id). \
        first()


def get_comment_like_count_by_uuid(session: Session, comment_uuid: UUID) -> int | None:
    return session.query(Comment).filter(Comment.uuid == comment_uuid).first().comment_like_associations.len()


def get_comment_save_by_id(session: Session, user_id: int, comment_id: int) -> Type[CommentSave] | None:
    return session.query(CommentSave). \
        filter(CommentSave.user_id == user_id
               and CommentSave.comment_id == comment_id). \
        first()


def get_comment_save_count_by_uuid(session: Session, comment_uuid: UUID) -> int | None:
    return session.query(Comment).filter(Comment.uuid == comment_uuid).first().comment_save_associations.len()
