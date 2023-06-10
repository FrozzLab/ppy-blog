from datetime import datetime
from uuid import UUID

from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import registry, Mapped, mapped_column, relationship

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


@mapper_registry.mapped
class User:
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column("uuid")
    first_name: Mapped[str] = mapped_column("first_name")
    last_name: Mapped[str] = mapped_column("last_name")
    profile_name: Mapped[str] = mapped_column("profile_name")
    email: Mapped[str] = mapped_column("email")
    password: Mapped[str] = mapped_column("password")
    country: Mapped[str] = mapped_column("country")
    created_at: Mapped[datetime] = mapped_column("created_at")
    blogs: Mapped[list["Blog"]] = relationship(
        secondary="user_blog",
        back_populates="owners"
    )
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    follow_associations: Mapped[list["UserFollowing"]] = relationship(
        primaryjoin="UserFollowing.follower_id==User.id",
        secondaryjoin="UserFollowing.user_id==User.id",
        back_populates="follower"
    )
    follower_associations: Mapped[list["UserFollowing"]] = relationship(
        primaryjoin="UserFollowing.user_id==User.id",
        secondaryjoin="UserFollowing.follower_id==User.id",
        back_populates="user"
    )
    blog_like_associations: Mapped[list["BlogLike"]] = relationship(back_populates="user")
    blog_save_associations: Mapped[list["BlogSave"]] = relationship(back_populates="user")
    post_like_associations: Mapped[list["PostLike"]] = relationship(back_populates="user")
    post_save_associations: Mapped[list["PostSave"]] = relationship(back_populates="user")
    comment_like_associations: Mapped[list["CommentLike"]] = relationship(back_populates="user")
    comment_save_associations: Mapped[list["CommentSave"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User: {self.id} {self.first_name} {self.last_name}"


@mapper_registry.mapped
class UserFollowing:
    __tablename__ = "following"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="follow_associations", foreign_keys=[user_id])
    follower_id: Mapped[int] = mapped_column("follower_id", ForeignKey("app_user.id"), primary_key=True)
    follower: Mapped["User"] = relationship(back_populates="follower_associations", foreign_keys=[follower_id])
    followed_at: Mapped[datetime] = mapped_column("followed_at")

    def __repr__(self):
        return f"UserFollowing: {self.user_id} {self.follower_id} {self.followed_at}"


@mapper_registry.mapped
class UserBlog:
    __tablename__ = "user_blog"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship()
    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"), primary_key=True)
    blog: Mapped["Blog"] = relationship()

    def __repr__(self):
        return f"UserBlog: {self.user_id} {self.blog_id}"


@mapper_registry.mapped
class Blog:
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column("uuid")
    title: Mapped[str] = mapped_column("title")
    description: Mapped[str] = mapped_column("description")
    created_at: Mapped[datetime] = mapped_column("created_at")
    owners: Mapped[list["User"]] = relationship(
        secondary="user_blog",
        back_populates="blogs"
    )
    posts: Mapped[list["Post"]] = relationship(back_populates="blog")
    blog_like_associations: Mapped[list["BlogLike"]] = relationship(back_populates="blog")
    blog_save_associations: Mapped[list["BlogSave"]] = relationship(back_populates="blog")

    def __repr__(self):
        return f"Blog: {self.id} {self.title}"


@mapper_registry.mapped
class BlogLike:
    __tablename__ = "blog_like"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="blog_like_associations")
    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"), primary_key=True)
    blog: Mapped["Blog"] = relationship(back_populates="blog_like_associations")
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.blog_id} {self.liked_at}"


@mapper_registry.mapped
class BlogSave:
    __tablename__ = "blog_save"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="blog_save_associations")
    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"), primary_key=True)
    blog: Mapped["Blog"] = relationship(back_populates="blog_save_associations")
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.blog_id} {self.saved_at}"


@mapper_registry.mapped
class Post:
    __tablename__ = "post"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column("uuid")
    blog_id: Mapped[int] = mapped_column("blog_id", ForeignKey("blog.id"))
    blog: Mapped["Blog"] = relationship(back_populates="posts")
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("app_user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    title: Mapped[str] = mapped_column("title")
    body: Mapped[str] = mapped_column("body")
    created_at: Mapped[datetime] = mapped_column("created_at")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    post_like_associations: Mapped[list["PostLike"]] = relationship(back_populates="post")
    post_save_associations: Mapped[list["PostSave"]] = relationship(back_populates="post")

    def __repr__(self):
        return f"Post: {self.id} {self.title}"


@mapper_registry.mapped
class PostLike:
    __tablename__ = "post_like"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="post_like_associations")
    post_id: Mapped[int] = mapped_column("post_id", ForeignKey("post.id"), primary_key=True)
    post: Mapped["Post"] = relationship(back_populates="post_like_associations")
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.post_id} {self.liked_at}"


@mapper_registry.mapped
class PostSave:
    __tablename__ = "post_save"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="post_save_associations")
    post_id: Mapped[int] = mapped_column("post_id", ForeignKey("post.id"), primary_key=True)
    post: Mapped["Post"] = relationship(back_populates="post_save_associations")
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.post_id} {self.saved_at}"


@mapper_registry.mapped
class Comment:
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column("uuid")
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("app_user.id"))
    user: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column("post_id", ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    body: Mapped[str] = mapped_column("body")
    created_at: Mapped[datetime] = mapped_column("created_at")
    comment_like_associations: Mapped[list["CommentLike"]] = relationship(back_populates="comment")
    comment_save_associations: Mapped[list["CommentSave"]] = relationship(back_populates="comment")

    def __repr__(self):
        return f"Comment: {self.id} {self.body}"


@mapper_registry.mapped
class CommentLike:
    __tablename__ = "comment_like"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="comment_like_associations")
    comment_id: Mapped[int] = mapped_column("comment_id", ForeignKey("comment.id"), primary_key=True)
    comment: Mapped["User"] = relationship(back_populates="comment_like_associations")
    liked_at: Mapped[datetime] = mapped_column("liked_at")

    def __repr__(self):
        return f"BlogLike: {self.user_id} {self.comment_id} {self.liked_at}"


@mapper_registry.mapped
class CommentSave:
    __tablename__ = "comment_save"

    user_id: Mapped[int] = mapped_column("app_user_id", ForeignKey("app_user.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="comment_save_associations")
    comment_id: Mapped[int] = mapped_column("comment_id", ForeignKey("comment.id"), primary_key=True)
    comment: Mapped["User"] = relationship(back_populates="comment_save_associations")
    saved_at: Mapped[datetime] = mapped_column("saved_at")

    def __repr__(self):
        return f"BlogSave: {self.user_id} {self.comment_id} {self.saved_at}"


def get_metadata():
    return metadata
