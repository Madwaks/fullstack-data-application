from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Exercise 1 – Hello World API
# -----------------------------
@app.get("/hello")
def hello_world():
    pass


# -----------------------------
# Exercise 2 – Path Parameters
# -----------------------------
@app.get("/hello/{name}")
def hello_user(name: str):
    pass


# -----------------------------
# Exercise 3 – Query Parameters
# -----------------------------
@app.get("/square")
def square(number: int):
    # TODO: return {"result": number * number}
    pass


# -----------------------------
# Exercise 4 – POST with Request Body
# -----------------------------
class Numbers(BaseModel):
    a: int
    b: int


@app.post("/sum")
def sum_numbers(payload: Numbers):
    # TODO: return {"result": payload.a + payload.b}
    pass


# -----------------------------
# Exercise 5 – Path + Query Together
# -----------------------------
@app.get("/items/{item_id}")
def get_item_with_details(item_id: int, details: bool = False):
    # TODO:
    # if details:
    #    return {"item_id": item_id, "description": "More details here"}
    # else:
    #    return {"item_id": item_id}
    pass


# -----------------------------
# Exercise 6 – Simple CRUD (in-memory list)
# -----------------------------
items = []  # in-memory store


@app.get("/crud/items")
def list_items():
    # TODO: return all items
    pass


@app.post("/crud/items")
def create_item(name: str):
    # TODO: append to list and return item
    pass


@app.delete("/crud/items/{item_id}")
def delete_item(item_id: int):
    # TODO: remove item by index
    pass


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
