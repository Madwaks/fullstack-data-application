# TP DATABASE

### Learning Objectives
- Create tables in SQL.
- Define primary and foreign keys.
- Insert and update records.
- Alter tables.

### Step 0: Prerequisites

In `docker-compose.yml`, create a service `db` with `postgres` image.

The postgres service needs some base environment variables to work:
- POSTGRES_USER="user"
- POSTGRES_PASSWORD="postgrespassword"
- POSTGRES_DB="dbesiee"

You will also need a volume to keep changes. Attach a volume to your service by adding: `postgres_data:/var/lib/postgresql/data` in the volume section of the compose file

Make sure the service runs by running
```
cd <path to>/02-database/tp
docker compose up -d
docker ps
```

In the following exercises you will have to open a shell in the Database.

```
docker compose exec db psql -U user -d dbesiee
```

_The psql shell is an interactive terminal for PostgreSQL. 
It allows you to connect to a PostgreSQL database and run SQL commands directly. 
With psql, you can create and manage tables, insert and query data, update records, and alter schemas. It also supports meta-commands (like \dt to list tables, \d table_name to see table details, and \q to quit) that make database exploration easier. It’s a powerful tool for both learning SQL and managing databases in practice._

### Step 1: Create Tables

Exercise 1: Create a USER table with the following columns:
- id (integer, primary key, auto-increment)
- first_name: 50 characters long, non nullable 
- last_name: 50 characters long, non nullable
- email: 100 characters long, unique and non nullable

Exercise 2: Create a BlogPost table with:
- id (integer, primary key, auto-increment)
- title: 200 characters long, non nullable
- content: text with character limitation, not nullable
- created_at: date with time
- user_id: foreign key

### Step 2: Insert Records

Exercise 3: Insert at least 3 users into the Users table.

Exercise 4: Insert 3 blog posts written by these users.

### Step 3: Update Records

Exercise 5: Update a user’s email address.

Exercise 6: Update a blog post’s title.

### Step 4: Alter Tables (Update Schema)

Exercise 7: Add a new column bio (text) to the Users table.

Exercise 8: Add a new column updated_at (datetime) to the BlogPost table.
Exercise 8bis: Add a trigger to automatically fill this new column when there is an update on the record

### Step 5: Select data
- Retrieve all blog posts written by a given author.
- Count how many blog posts each user has written.

### Step 6: Batch Execution

Write all the commands in a file and execute all of them at once.