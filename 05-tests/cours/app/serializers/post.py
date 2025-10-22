from pydantic import BaseModel, ConfigDict

from serializers import User


class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str | None
    author_id: str


class PostWithAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    content: str
    author: User
