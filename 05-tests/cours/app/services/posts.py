from datetime import datetime

from sqlalchemy.exc import IntegrityError

import models
import serializers
from sqlalchemy.orm import Session

from services import user as user_service
from exceptions.post import PostNotFound, PostAlreadyExists, WrongAuthor


def get_all_posts(db: Session, skip: int = 0, limit: int = 10) -> list[models.Post]:
    records = db.query(models.Post).offset(skip).limit(limit).all()
    for record in records:
        record.id = str(record.id)
    return records


def get_post_by_id(post_id: str, db: Session) -> models.Post:
    record = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not record:
        raise PostNotFound

    record.id = str(record.id)
    return record


def get_posts_by_title(title: str, db: Session) -> list[models.Post]:
    records = db.query(models.Post).filter(models.Post.title == title).all()
    for record in records:
        record.id = str(record.id)
    return records


def update_post(post_id: str, db: Session, post: serializers.Post) -> models.Post:
    db_post = get_post_by_id(post_id=post_id, db=db)
    for var, value in vars(post).items():
        setattr(db_post, var, value) if value else None
    db_post.updated_at = datetime.now()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(post_id: str, db: Session) -> models.Post:
    db_post = get_post_by_id(post_id=post_id, db=db)
    db.delete(db_post)
    db.commit()
    return db_post


def delete_post_by_user(post_id: str, db: Session, user_id: str) -> models.Post:
    db_post = get_post_by_id(post_id=post_id, db=db)
    if db_post.author_id != user_id:
        raise WrongAuthor
    db.delete(db_post)
    db.commit()
    return db_post


def delete_all_posts(db: Session) -> list[models.Post]:
    records = db.query(models.Post).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records


def create_post(db: Session, post: serializers.Post) -> models.Post:
    author_id = post.author_id

    # Peut raise un UserNotFound
    user_service.get_user_by_id(user_id=author_id, db=db)

    db_post = models.Post(**post.model_dump())
    db.add(db_post)

    try:
        db.commit()
    except IntegrityError:
        raise PostAlreadyExists

    db.refresh(db_post)

    return db_post
