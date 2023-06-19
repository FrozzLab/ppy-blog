from datetime import datetime

from src.backend.schemas.base_schemas import UserBaseSchema, BlogBaseSchema, PostBaseSchema, CommentBaseSchema
from src.backend.schemas.create_schemas import BlogLikeCreateSchema, PostLikeCreateSchema, BlogSaveCreateSchema, \
    PostSaveCreateSchema, CommentLikeCreateSchema, CommentSaveCreateSchema


class UserGetSchema(UserBaseSchema):
    blogs: list[BlogBaseSchema]


class BlogGetSchema(BlogBaseSchema):
    owners: list[UserBaseSchema]
    posts: list[PostBaseSchema]


class PostGetSchema(PostBaseSchema):
    pass


class CommentGetSchema(CommentBaseSchema):
    pass


class BlogLikeGetSchema(BlogLikeCreateSchema):
    liked_at: datetime


class PostLikeGetSchema(PostLikeCreateSchema):
    liked_at: datetime


class BlogSaveGetSchema(BlogSaveCreateSchema):
    saved_at: datetime


class PostSaveGetSchema(PostSaveCreateSchema):
    saved_at: datetime


class CommentLikeGetSchema(CommentLikeCreateSchema):
    liked_at: datetime


class CommentSaveGetSchema(CommentSaveCreateSchema):
    saved_at: datetime
