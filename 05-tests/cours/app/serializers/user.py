from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str


class UserOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: str
