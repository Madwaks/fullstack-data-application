from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI(
    title="01-api",
    description="My description",
    version="0.0.1",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Numbers(BaseModel):
    a: int
    b: int


@app.post("/sum")
def sum_numbers(payload: Numbers):
    return {"result": payload.a + payload.b}
