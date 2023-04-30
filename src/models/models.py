from datetime import datetime

from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import registry, Mapped, mapped_column

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


@mapper_registry.mapped
class User:
    __tablename__ = "app_user"

    first_name: Mapped[str] = mapped_column("first_name")
    last_name: Mapped[str] = mapped_column("last_name")
    profile_name: Mapped[str] = mapped_column("profile_name")
    email: Mapped[str] = mapped_column("email")
    password: Mapped[str] = mapped_column("password")
    country: Mapped[str] = mapped_column("country")
    signup_date: Mapped[datetime] = mapped_column("signup_date")
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"User: {self.id} {self.first_name} {self.last_name}"


@mapper_registry.mapped
class UserFollowing:
    __tablename__ = "following"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("follower_id"), primary_key=True)
    followed_at: Mapped[datetime] = mapped_column("followed_at")

    def __repr__(self):
        return f"UserFollowing: {self.user_id} {self.follower_id} {self.followed_at}"


@mapper_registry.mapped
class UserBlog:
    __tablename__ = "user_blog"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    blog_id: Mapped[int] = mapped_column(ForeignKey("blog_id"), primary_key=True)

    def __repr__(self):
        return f"UserFollowing: {self.user_id} {self.blog_id}"


@mapper_registry.mapped
class Blog:
    __tablename__ = "blog"

    title: Mapped[str] = mapped_column("title")
    description: Mapped[str] = mapped_column("description")
    created_at: Mapped[datetime] = mapped_column("created_at")
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Blog: {self.id} {self.title}"


@mapper_registry.mapped
class BlogLike:
    __tablename__ = "blog_like"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    blog_id: Mapped[int] = mapped_column(ForeignKey("blog_id"), primary_key=True)
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.blog_id} {self.liked_at}"


@mapper_registry.mapped
class BlogSave:
    __tablename__ = "blog_save"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    blog_id: Mapped[int] = mapped_column(ForeignKey("blog_id"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.blog_id} {self.saved_at}"


@mapper_registry.mapped
class Post:
    __tablename__ = "post"

    blog_id: Mapped[int] = mapped_column(ForeignKey("blog_id"))
    title: Mapped[str] = mapped_column("title")
    body: Mapped[str] = mapped_column("body")
    created_at: Mapped[datetime] = mapped_column("created_at")
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Post: {self.id} {self.title}"


@mapper_registry.mapped
class PostLike:
    __tablename__ = "post_like"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post_id"), primary_key=True)
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.post_id} {self.liked_at}"


@mapper_registry.mapped
class PostSave:
    __tablename__ = "post_save"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post_id"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.post_id} {self.saved_at}"


@mapper_registry.mapped
class Comment:
    __tablename__ = "comment"

    post_id: Mapped[int] = mapped_column(ForeignKey("post_id"))
    body: Mapped[str] = mapped_column("body")
    created_at: Mapped[datetime] = mapped_column("created_at")
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Comment: {self.id} {self.body}"


@mapper_registry.mapped
class CommentLike:
    __tablename__ = "comment_like"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comment_id"), primary_key=True)
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.comment_id} {self.liked_at}"


@mapper_registry.mapped
class CommentSave:
    __tablename__ = "comment_save"

    user_id: Mapped[int] = mapped_column(ForeignKey("app_user_id"), primary_key=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comment_id"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.comment_id} {self.saved_at}"


def get_metadata():
    return metadata


def get_mapper_registry():
    return mapper_registry
