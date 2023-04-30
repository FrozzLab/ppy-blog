from datetime import datetime

from pydantic import BaseModel


class UserIdSchema(BaseModel):
    user_id: int


class InteractionSchema(UserIdSchema):
    content_id: int
    interacted_with_at: datetime


class UserSchema(UserIdSchema):
    first_name: str
    last_name: str
    email: str
    password: str
    country: str
    signup_date: datetime


class UserFollowingSchema(UserIdSchema):
    follower_id: int
    followed_at: datetime


class UserBlogSchema(UserIdSchema):
    blog_id: int


class BlogSchema:
    title: str
    description: str
    created_at: datetime
    id: str


class PostSchema:
    blog_id: int
    title: str
    body: str
    created_at: datetime
    id: int


class CommentSchema:
    post_id: int
    body: str
    created_at: datetime
    id: int
