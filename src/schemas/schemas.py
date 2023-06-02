from datetime import datetime

from pydantic import BaseModel
from pydantic.schema import Optional


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


class UserUpdateSchema(OrmBaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    profile_name: Optional[str]
    email: Optional[str]
    country: Optional[str]


class UserLoginSchema(OrmBaseModel):
    profile_name: str
    password: str


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


class BlogUpdateSchema(OrmBaseModel):
    title: Optional[str]
    description: Optional[str]


class PostBaseSchema(OrmBaseModel):
    blog_id: int
    title: str
    body: str


class PostCreateSchema(PostBaseSchema):
    pass


class PostGetSchema(PostBaseSchema):
    id: int
    created_at: datetime


class PostUpdateSchema(OrmBaseModel):
    title: Optional[str]
    body: Optional[str]


class CommentBaseSchema(OrmBaseModel):
    user_id: int
    post_id: int
    body: str


class CommentCreateSchema(CommentBaseSchema):
    pass


class CommentGetSchema(CommentBaseSchema):
    id: int
    created_at: datetime


class CommentUpdateSchema(OrmBaseModel):
    body: Optional[str]


class LikeBaseSchema(OrmBaseModel):
    user_id: int


class BlogLikeCreateSchema(LikeBaseSchema):
    blog_id: int


class BlogLikeGetSchema(BlogLikeCreateSchema):
    liked_at: datetime


class PostLikeCreateSchema(LikeBaseSchema):
    post_id: int


class PostLikeGetSchema(PostLikeCreateSchema):
    liked_at: datetime


class CommentLikeCreateSchema(LikeBaseSchema):
    comment_id: int


class CommentLikeGetSchema(CommentLikeCreateSchema):
    liked_at: datetime


class SaveBaseSchema(OrmBaseModel):
    user_id: int


class BlogSaveCreateSchema(SaveBaseSchema):
    blog_id: int


class BlogSaveGetSchema(BlogSaveCreateSchema):
    saved_at: datetime


class PostSaveCreateSchema(SaveBaseSchema):
    post_id: int


class PostSaveGetSchema(PostSaveCreateSchema):
    saved_at: datetime


class CommentSaveCreateSchema(SaveBaseSchema):
    comment_id: int


class CommentSaveGetSchema(CommentSaveCreateSchema):
    saved_at: datetime
