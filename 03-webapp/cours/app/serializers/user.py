from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class UserOutput(BaseModel):
    id: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
