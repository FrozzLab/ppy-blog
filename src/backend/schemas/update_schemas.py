import re

from pydantic import Field
from pydantic.class_validators import validator
from pydantic.schema import Optional

from src.backend.schemas.base_schemas import OrmBaseModel


# noinspection PyMethodParameters
class UserUpdateSchema(OrmBaseModel):
    first_name: Optional[str] = Field(min_length=2, max_length=30)
    last_name: Optional[str] = Field(min_length=2, max_length=30)
    profile_name: Optional[str] = Field(min_length=4, max_length=20)
    country: Optional[str]

    @validator('profile_name')
    def profile_name_is_valid(cls, profile_name):
        regex_profile_name = re.compile('^([a-z0-9]|[-._](?![-._])){4,20}$')
        if regex_profile_name.match(profile_name) is None:
            raise ValueError('Username must be between 4 and 20 characters long, '
                             'and may not contain non-alphanumeric symbols apart '
                             'from . and _, which may not be used consecutively.')
        return profile_name


class BlogUpdateSchema(OrmBaseModel):
    title: Optional[str] = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=200)


class PostUpdateSchema(OrmBaseModel):
    title: Optional[str] = Field(min_length=2, max_length=100)
    body: Optional[str] = Field(min_length=1, max_length=4000)


class CommentUpdateSchema(OrmBaseModel):
    body: Optional[str] = Field(min_length=1, max_length=1000)
