from datetime import datetime

from pydantic import BaseModel


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserBaseSchema(OrmBaseModel):
    first_name: str
    last_name: str
    profile_name: str
    email: str
    country: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserGetSchema(UserBaseSchema):
    id: int
    signup_date: datetime


class UserFollowingSchema(OrmBaseModel):
    user_id: int
    follower_id: int
    followed_at: datetime


class UserBlogSchema(OrmBaseModel):
    user_id: int
    blog_id: int


class InteractionSchema(OrmBaseModel):
    user_id: int
    content_id: int
    interacted_with_at: datetime


class BlogBaseSchema(OrmBaseModel):
    title: str
    description: str


class BlogCreateSchema(BlogBaseSchema):
    pass


class BlogGetSchema(BlogCreateSchema):
    id: str
    created_at: datetime


class PostBaseSchema(OrmBaseModel):
    blog_id: int
    title: str
    body: str


class PostCreateSchema(PostBaseSchema):
    pass


class PostGetSchema(PostBaseSchema):
    id: int
    created_at: datetime


class CommentBaseSchema(OrmBaseModel):
    user_id: int
    post_id: int
    body: str


class CommentCreateSchema(CommentBaseSchema):
    pass


class CommentGetSchema(CommentBaseSchema):
    id: int
    created_at: datetime
