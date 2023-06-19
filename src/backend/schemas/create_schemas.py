import re

from pydantic import Field
from pydantic.class_validators import validator
from pydantic.networks import EmailStr

from src.backend.schemas.base_schemas import OrmBaseModel, SaveBaseSchema, LikeBaseSchema


# noinspection PyMethodParameters
class UserCreateSchema(OrmBaseModel):
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    profile_name: str = Field(min_length=4, max_length=20)
    password: str
    email: EmailStr
    country: str

    @validator('password')
    def password_is_valid(cls, password):
        regex_pass = re.compile('^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
        if regex_pass.match(password) is None:
            raise ValueError('Password must be between 8 and 20 characters long, '
                             'and must contain a number and a special character.')
        return password

    @validator('profile_name')
    def profile_name_is_valid(cls, profile_name):
        regex_profile_name = re.compile('^([a-zA-Z0-9]|[-._](?![-._])){4,20}$')
        if regex_profile_name.match(profile_name) is None:
            raise ValueError('Username must be between 4 and 20 characters long, '
                             'and may not contain non-alphanumeric symbols apart '
                             'from . and _, which may not be used consecutively.')
        return profile_name


class BlogCreateSchema(OrmBaseModel):
    user_id: int
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=1, max_length=200)


class PostCreateSchema(OrmBaseModel):
    user_id: int
    blog_id: int
    title: str = Field(min_length=2, max_length=100)
    body: str = Field(min_length=1, max_length=4000)


class CommentCreateSchema(OrmBaseModel):
    user_id: int
    post_id: int
    body: str = Field(min_length=1, max_length=1000)


class BlogLikeCreateSchema(LikeBaseSchema):
    blog_id: int


class PostLikeCreateSchema(LikeBaseSchema):
    post_id: int


class CommentLikeCreateSchema(LikeBaseSchema):
    comment_id: int


class BlogSaveCreateSchema(SaveBaseSchema):
    blog_id: int


class PostSaveCreateSchema(SaveBaseSchema):
    post_id: int


class CommentSaveCreateSchema(SaveBaseSchema):
    comment_id: int
