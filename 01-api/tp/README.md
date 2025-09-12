# Exercise 1 – Hello World API
- Create a FastAPI app with a single route /hello returning a JSON message.
- Example: {"message": "Hello, API World!"}

# Exercise 2 – Path Parameters
- Add a route /greet/{name} that takes a name in the URL and returns {"message": "Hello <name>"}.
- Try with different names in the path.


# Exercise 3 – Query Parameters
- Create a route /square with a query parameter ?number=4 that returns the square of the number.
Example: /square?number=5 → {"result": 25}

# Exercise 4 – POST with Request Body
- Create a route /sum that accepts a JSON body like:
  - Use Pydantic model to serialize the input body

{"a": 4, "b": 7} and returns {"result": 11}.

# Exercise 5 – Simple CRUD (in-memory list)
	•	Keep a Python list of items (items = []).
	•	Implement routes:
	•	GET /items → list all items
	•	POST /items → add an item ({"name": "book"})
	•	DELETE /items/{id} → remove by index
Goal: Simulate CRUD without a database.

# Exercise 6 – Response Models
- Define a Pydantic model for User with id, name, age.
- Create a route /user/{id} returning a hardcoded user.
Goal: Show structured responses and response_model validation.

# Exercise 7 – Error Handling
- Modify one of the CRUD routes so that if a user requests an invalid ID, the API returns:

{"error": "Item not found"}

with status code 404.