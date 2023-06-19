from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.backend.models.models import User, Blog, Post, Comment, BlogLike, PostLike, CommentLike, BlogSave, PostSave, \
    CommentSave


def delete_user_by_uuid(session: Session, user_uuid: UUID) -> None:
    session.query(User).filter(User.uuid == user_uuid).delete()
    session.commit()


def delete_blog_by_uuid(session: Session, blog_uuid: UUID) -> None:
    session.query(Blog).filter(Blog.uuid == blog_uuid).delete()
    session.commit()


def delete_post_by_uuid(session: Session, post_uuid: UUID) -> None:
    session.query(Post).filter(Post.uuid == post_uuid).delete()
    session.commit()


def delete_comment_by_uuid(session: Session, comment_uuid: UUID) -> None:
    session.query(Comment).filter(Comment.uuid == comment_uuid).delete()
    session.commit()


def delete_blog_like_by_uuid(session: Session, user_uuid: UUID, blog_uuid: UUID) -> None:
    session.query(BlogLike). \
        filter(BlogLike.user_uuid == user_uuid
               and BlogLike.blog_uuid == blog_uuid). \
        delete()

    session.commit()


def delete_post_like_by_uuid(session: Session, user_uuid: UUID, post_uuid: UUID) -> None:
    session.query(PostLike). \
        filter(PostLike.user_uuid == user_uuid
               and PostLike.post_uuid == post_uuid). \
        delete()

    session.commit()


def delete_comment_like_by_uuid(session: Session, user_uuid: UUID, comment_uuid: UUID) -> None:
    session.query(CommentLike). \
        filter(CommentLike.user_uuid == user_uuid
               and CommentLike.comment_uuid == comment_uuid). \
        delete()

    session.commit()


def delete_blog_save_by_uuid(session: Session, user_uuid: UUID, blog_uuid: UUID) -> None:
    session.query(BlogSave). \
        filter(BlogSave.user_uuid == user_uuid
               and BlogSave.blog_uuid == blog_uuid). \
        delete()

    session.commit()


def delete_post_save_by_uuid(session: Session, user_uuid: UUID, post_uuid: UUID) -> None:
    session.query(PostSave). \
        filter(PostSave.user_uuid == user_uuid
               and PostSave.post_uuid == post_uuid). \
        delete()

    session.commit()


def delete_comment_save_by_uuid(session: Session, user_uuid: UUID, comment_uuid: UUID) -> None:
    session.query(CommentSave). \
        filter(CommentSave.user_uuid == user_uuid
               and CommentSave.comment_uuid == comment_uuid). \
        delete()

    session.commit()
