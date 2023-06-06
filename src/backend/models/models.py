from datetime import datetime

from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import registry, Mapped, mapped_column, relationship

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


@mapper_registry.mapped
class User:
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column("first_name")
    last_name: Mapped[str] = mapped_column("last_name")
    profile_name: Mapped[str] = mapped_column("profile_name")
    email: Mapped[str] = mapped_column("email")
    password: Mapped[str] = mapped_column("password")
    country: Mapped[str] = mapped_column("country")
    signup_date: Mapped[datetime] = mapped_column("signup_date")
    blogs: Mapped[list["Blog"]] = relationship(
        "Blog",
        secondary="user_blog",
        back_populates="owners"
    )

    def __repr__(self):
        return f"User: {self.id} {self.first_name} {self.last_name}"


@mapper_registry.mapped
class UserFollowing:
    __tablename__ = "following"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    follower_id: Mapped[int] = mapped_column("follower_id", ForeignKey("app_user.id"), primary_key=True)
    followed_at: Mapped[datetime] = mapped_column("followed_at")

    def __repr__(self):
        return f"UserFollowing: {self.user_id} {self.follower_id} {self.followed_at}"


@mapper_registry.mapped
class UserBlog:
    __tablename__ = "user_blog"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"), primary_key=True)

    def __repr__(self):
        return f"UserBlog: {self.user_id} {self.blog_id}"


@mapper_registry.mapped
class Blog:
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column("title")
    description: Mapped[str] = mapped_column("description")
    created_at: Mapped[datetime] = mapped_column("created_at")
    owners: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_blog",
        back_populates="blogs"
    )

    def __repr__(self):
        return f"Blog: {self.id} {self.title}"


@mapper_registry.mapped
class BlogLike:
    __tablename__ = "blog_like"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"), primary_key=True)
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.blog_id} {self.liked_at}"


@mapper_registry.mapped
class BlogSave:
    __tablename__ = "blog_save"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.blog_id} {self.saved_at}"


@mapper_registry.mapped
class Post:
    __tablename__ = "post"

    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"))
    title: Mapped[str] = mapped_column("title")
    body: Mapped[str] = mapped_column("body")
    created_at: Mapped[datetime] = mapped_column("created_at")
    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Post: {self.id} {self.title}"


@mapper_registry.mapped
class PostLike:
    __tablename__ = "post_like"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    post_id: Mapped[int] = mapped_column("post_id", ForeignKey("post.id"), primary_key=True)
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.post_id} {self.liked_at}"


@mapper_registry.mapped
class PostSave:
    __tablename__ = "post_save"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    post_id: Mapped[int] = mapped_column("post_id", ForeignKey("post.id"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.post_id} {self.saved_at}"


@mapper_registry.mapped
class Comment:
    __tablename__ = "comment"

    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("app_user.id"))
    post_id: Mapped[int] = mapped_column("post_id", ForeignKey("post.id"))
    body: Mapped[str] = mapped_column("body")
    created_at: Mapped[datetime] = mapped_column("created_at")
    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"Comment: {self.id} {self.body}"


@mapper_registry.mapped
class CommentLike:
    __tablename__ = "comment_like"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    comment_id: Mapped[int] = mapped_column("comment_id", ForeignKey("comment.id"), primary_key=True)
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.comment_id} {self.liked_at}"


@mapper_registry.mapped
class CommentSave:
    __tablename__ = "comment_save"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    comment_id: Mapped[int] = mapped_column("comment_id", ForeignKey("comment.id"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.comment_id} {self.saved_at}"


def get_metadata():
    return metadata
