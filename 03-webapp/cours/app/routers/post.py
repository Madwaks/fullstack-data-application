import models
import serializers
import database
from fastapi import APIRouter, Depends, HTTPException

from exceptions.post import PostNotFound, PostAlreadyExists
from exceptions.user import UserNotFound
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
async def delete_post_by_id(post_id: str, db: Session = Depends(database.get_db)):
    try:
        return posts_service.delete_post(post_id=post_id, db=db)
    except PostNotFound:
        raise HTTPException(status_code=404, detail="Post not found")


@post_router.delete("/", tags=["posts"])
async def delete_all_posts(db: Session = Depends(database.get_db)):
    return posts_service.delete_all_posts(db=db)
