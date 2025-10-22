from typing import Union

from fastapi import Header, HTTPException

from services.auth import decode_jwt


async def verify_authorization_header(
    authorization: str = Header(...),
) -> dict[str, Union[int, dict[str, Union[list[str], int, str]]]]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No authorization header")

    return decode_jwt(authorization.split("Bearer ")[1])


async def get_user_id(authorization: str = Header(...)) -> str:
    auth = await verify_authorization_header(authorization)
    try:
        user_id = str(auth["user_id"])
    except KeyError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id
