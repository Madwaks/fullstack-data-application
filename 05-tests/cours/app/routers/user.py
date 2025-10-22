import serializers
import database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from exceptions.user import UserNotFound
from services import user as user_service

user_router = APIRouter(prefix="/users")


@user_router.post("/", tags=["users"])
async def create_user(
    user: serializers.User, db: Session = Depends(database.get_db)
) -> serializers.UserOutput:
    return user_service.create_user(user=user, db=db)


@user_router.get("/", tags=["users"])
async def get_all_users(db: Session = Depends(database.get_db)):
    return user_service.get_all_users(db=db)


@user_router.delete("/{user_id}", tags=["users"])
async def delete_user_by_id(user_id: str, db: Session = Depends(database.get_db)):
    try:
        return user_service.delete_user(user_id=user_id, db=db)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
