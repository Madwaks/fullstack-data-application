from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Exercise 1 – Hello World API
# -----------------------------
@app.get("/hello")
def hello_world():
    return {"message": "Hello, API World!"}


# -----------------------------
# Exercise 2 – Path Parameters
# -----------------------------
@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello {name}"}


# -----------------------------
# Exercise 3 – Query Parameters
# -----------------------------
@app.get("/square")
def square(number: int):
    return {"result": number * number}


# -----------------------------
# Exercise 4 – POST with Request Body
# -----------------------------
class Numbers(BaseModel):
    a: int
    b: int


@app.post("/sum")
def sum_numbers(payload: Numbers):
    return {"result": payload.a + payload.b}


# -----------------------------
# Exercise 5 – Simple CRUD (in-memory list)
# -----------------------------
items = []  # in-memory store


class Item(BaseModel):
    name: str
    value: int


@app.get("/crud/items", response_model=list[Item])
def list_items():
    return [item for item in items]


@app.post("/crud/items")
def create_item(item: Item):
    items.append(item)
    return item


@app.delete("/crud/items/{item_id}")
def delete_item(item_id: int):
    item = items.pop(item_id)
    return item


# -----------------------------
# Exercise 7 – Response Models
# -----------------------------
class User(BaseModel):
    id: int
    name: str
    age: int


@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int):
    # TODO: return a hardcoded User
    pass


# -----------------------------
# Exercise 8 – Error Handling
# -----------------------------
items_with_data = ["apple", "banana", "cherry"]


@app.get("/safe/items/{item_id}")
def get_item_safe(item_id: int):
    # TODO:
    # if item_id invalid -> raise HTTPException(status_code=404, detail="Item not found")
    # else return the item
    pass
