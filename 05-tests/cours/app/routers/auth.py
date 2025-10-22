from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import database
from serializers.auth_token import AuthToken
from serializers import User
from services.auth import generate_access_token
from exceptions.user import UserNotFound, IncorrectPassword

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/token", tags=["auth"])
async def get_access_token(
    user_login: User,
    db: Session = Depends(database.get_db),
) -> AuthToken:
    try:
        access_token = generate_access_token(db=db, user_login=user_login)

    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IncorrectPassword as e:
        raise HTTPException(status_code=400, detail=str(e))
    return AuthToken(
        access_token=access_token,
    )
