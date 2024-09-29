from typing import List, Optional
from pydantic import BaseModel, create_model, ConfigDict
from enum import Enum
from functools import lru_cache

from typing import Type, TypeVar

T = TypeVar("T", bound=Enum)


def get_missing_includes(present_includes: List[T], includes_enum: Type[T]) -> List[T]:
    # Returns a list of enum values not present in the given list
    all_includes = set(includes_enum)
    present_includes_set = set(present_includes)
    missing_includes = all_includes - present_includes_set
    return list(missing_includes)


@lru_cache
def get_model(model_name, base: type[BaseModel], exclude_fields_set: frozenset):
    # Creates a new Pydantic model based on a base model, excluding specified fields
    fields = {
        field_name: (field.annotation, field)
        for field_name, field in base.model_fields.items()
        if field_name not in exclude_fields_set
    }

    return create_model(model_name, **fields, __config__=base.model_config)


def omit_model_fields(base: type[BaseModel], exclude_fields: List[str]):
    # Creates a new model by omitting specified fields from a base model
    exclude_fields_set = frozenset(exclude_fields)
    model_name = f"{base.__name__}_{hash(exclude_fields_set)}"

    return get_model(model_name, base, exclude_fields_set)


class TagBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    status: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class Post(PostBase):
    user: Optional[UserBase] = None
    tags: Optional[List[TagBase]] = None
    comments: Optional[List[CommentBase]] = None


class User(UserBase):
    posts: Optional[List[PostBase]] = None
    comments: Optional[List[CommentBase]] = None


class PostAllowedIncludes(str, Enum):
    tags = "tags"
    user = "user"
    comments = "comments"


class UserAllowedIncludes(str, Enum):
    posts = "posts"
    comments = "comments"


class PostFilter(BaseModel):
    include: Optional[List[PostAllowedIncludes]] = []


class PostsFilter(PostFilter):
    status: Optional[str] = None


class UserFilter(BaseModel):
    include: Optional[List[UserAllowedIncludes]] = []
