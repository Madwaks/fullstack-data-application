from pydantic import BaseModel

from serializers import User


class Post(BaseModel):
    title: str
    content: str | None
    author_id: str

    class Config:
        from_attributes = True


class PostWithAuthor(BaseModel):
    id: str
    title: str
    content: str
    author: User

    class Config:
        from_attributes = True
