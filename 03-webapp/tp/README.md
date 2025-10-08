# TP WEBAPP

### Step 0: Prerequisites

1. As usual, write a docker compose to run the API and a postgres database.
2. Optional: Write a script to fill the database with a few objects

### Step 1: Add route

Exercise 1: Allow a user to update a post
Exercise 1bis: Only the owner should be able to modify their post

### Step 2: Extends the models

Exercise 2: Add email field to User model, this field should be unique.
Exercise 2bis: Ensure the API responds correctly when trying to create an already existing user

Exercise 3: Add a model Comments to allow any user to add comments to a given Post

### Step 3: Filter a response

Exercise 4: Add or modify a route to return only the posts written by a given user

