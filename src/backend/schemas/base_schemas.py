from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserBaseSchema(OrmBaseModel):
    id: int
    uuid: UUID
    first_name: str
    last_name: str
    profile_name: str
    email: str
    country: str
    created_at: datetime


class BlogBaseSchema(OrmBaseModel):
    id: int
    uuid: UUID
    title: str
    description: str
    created_at: datetime


class PostBaseSchema(OrmBaseModel):
    id: int
    uuid: UUID
    user_id: int
    blog_id: int
    title: str
    body: str
    created_at: datetime


class CommentBaseSchema(OrmBaseModel):
    id: int
    uuid: UUID
    user_id: int
    post_id: int
    body: str
    created_at: datetime


class LikeBaseSchema(OrmBaseModel):
    user_id: int


class SaveBaseSchema(OrmBaseModel):
    user_id: int
