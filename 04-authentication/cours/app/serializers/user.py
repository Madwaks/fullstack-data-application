from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserOutput(BaseModel):
    id: str
    username: str

    class Config:
        from_attributes = True
