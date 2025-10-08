from sqlalchemy import Column, String, DateTime, Integer
import uuid

from sqlalchemy.orm import relationship

from database import BaseSQL


class User(BaseSQL):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    first_name = Column(String)
    last_name = Column(String)

    posts = relationship("Post", back_populates="author")
