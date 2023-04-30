from datetime import datetime

from pydantic import BaseModel
from pydantic.schema import Optional


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserIdSchema(OrmBaseModel):
    user_id: Optional[int]


class InteractionSchema(UserIdSchema):
    content_id: int
    interacted_with_at: datetime


class UserSchema(OrmBaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    country: str
    signup_date: datetime


class UserFollowingSchema(UserIdSchema):
    follower_id: int
    followed_at: datetime


class UserBlogSchema(UserIdSchema):
    blog_id: int


class BlogSchema(OrmBaseModel):
    title: str
    description: str
    created_at: datetime
    id: str


class PostSchema(OrmBaseModel):
    blog_id: int
    title: str
    body: str
    created_at: datetime
    id: int


class CommentSchema(OrmBaseModel):
    post_id: int
    body: str
    created_at: datetime
    id: int
