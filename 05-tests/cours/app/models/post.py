from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
import uuid

from sqlalchemy.orm import relationship

from database import BaseSQL


class Post(BaseSQL):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String)
    content = Column(String)

    author_id = Column(String, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")

    __table_args__ = (
        UniqueConstraint("title", "author_id", name="unique_author_post_title"),
    )
