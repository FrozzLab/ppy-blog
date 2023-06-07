from datetime import datetime

from pydantic import BaseModel
from pydantic.schema import Optional


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


#####
# Base Schemas
#####

class UserBaseSchema(OrmBaseModel):
    uuid: str
    first_name: str
    last_name: str
    profile_name: str
    email: str
    country: str
    created_at: datetime


class BlogBaseSchema(OrmBaseModel):
    uuid: str
    title: str
    description: str
    created_at: datetime


class PostBaseSchema(OrmBaseModel):
    uuid: str
    blog_uuid: str
    title: str
    body: str
    created_at: datetime


class CommentBaseSchema(OrmBaseModel):
    uuid: str
    user_uuid: str
    post_uuid: str
    body: str
    created_at: datetime


#####
# Create Schemas
#####

class UserCreateSchema(OrmBaseModel):
    first_name: str
    last_name: str
    profile_name: str
    password: str
    email: str
    country: str


class BlogCreateSchema(OrmBaseModel):
    title: str
    description: str


class PostCreateSchema(OrmBaseModel):
    blog_uuid: str
    title: str
    body: str


class CommentCreateSchema(OrmBaseModel):
    user_uuid: str
    post_uuid: str
    body: str


#####
# Get Schemas
#####

class UserGetSchema(UserBaseSchema):
    blogs: list[BlogBaseSchema]


class BlogGetSchema(BlogBaseSchema):
    owners: list[UserGetSchema]


class PostGetSchema(PostBaseSchema):
    pass


class CommentGetSchema(CommentBaseSchema):
    pass


#####
# Update Schemas
#####

class UserUpdateSchema(OrmBaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    profile_name: Optional[str]
    email: Optional[str]
    country: Optional[str]


class BlogUpdateSchema(OrmBaseModel):
    title: Optional[str]
    description: Optional[str]


class PostUpdateSchema(OrmBaseModel):
    title: Optional[str]
    body: Optional[str]


class CommentUpdateSchema(OrmBaseModel):
    body: Optional[str]


class UserFollowingSchema(OrmBaseModel):
    user_id: int
    follower_id: int
    followed_at: datetime

#####

class InteractionSchema(OrmBaseModel):
    user_id: int
    content_id: int
    interacted_with_at: datetime


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
