import serializers
import database
from fastapi import APIRouter, Depends, HTTPException

from exceptions.post import PostNotFound, PostAlreadyExists, WrongAuthor
from exceptions.user import UserNotFound
from routers.utils import get_user_id
from serializers.post import PostWithAuthor
from services import posts as posts_service
from sqlalchemy.orm import Session

post_router = APIRouter(prefix="/posts")


@post_router.post("/", tags=["posts"])
async def create_post(post: serializers.Post, db: Session = Depends(database.get_db)):
    try:
        return posts_service.create_post(post=post, db=db)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except PostAlreadyExists:
        raise HTTPException(status_code=409, detail="Post already exists")


@post_router.get("/", tags=["posts"], response_model=list[PostWithAuthor])
async def get_all_posts(db: Session = Depends(database.get_db)):
    return posts_service.get_all_posts(db=db)


@post_router.delete("/{post_id}", tags=["posts"])
async def delete_post_by_id(
    post_id: str,
    db: Session = Depends(database.get_db),
    user_id: str = Depends(get_user_id),
):
    try:
        return posts_service.delete_post_by_user(
            post_id=post_id, db=db, user_id=user_id
        )
    except PostNotFound:
        raise HTTPException(status_code=404, detail="Post not found")
    except WrongAuthor:
        raise HTTPException(status_code=403, detail="Only author can delete their post")


@post_router.delete("/", tags=["posts"])
async def delete_all_posts(db: Session = Depends(database.get_db)):
    return posts_service.delete_all_posts(db=db)
