import psycopg2
from psycopg2 import sql

# Superuser credentials (typically 'postgres')
superuser_connection = psycopg2.connect(
    dbname='postgres',  # Default admin database
    user='postgres',    # Superuser
    password='superuser_password',  # Replace with the actual password
    host='localhost'
)
superuser_connection.autocommit = True  # Required to create DB and user

# Create a cursor object using the superuser connection
superuser_cursor = superuser_connection.cursor()

# Database and user information
new_db_name = 'password_manager_db'
new_user_name = 'password_manager_user'
new_user_password = 'strong_password'

# 1. Create a new database
try:
    superuser_cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name))
    )
    print(f"Database '{new_db_name}' created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print(f"Database '{new_db_name}' already exists.")

# 2. Create a new user with a password
try:
    superuser_cursor.execute(
        sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(new_user_name)),
        [new_user_password]
    )
    print(f"User '{new_user_name}' created successfully.")
except psycopg2.errors.DuplicateObject:
    print(f"User '{new_user_name}' already exists.")

# 3. Grant privileges to the new user on the new database
try:
    superuser_cursor.execute(
        sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(new_db_name), sql.Identifier(new_user_name)
        )
    )
    print(f"Privileges granted to user '{new_user_name}' on database '{new_db_name}'.")
except Exception as e:
    print(f"Error granting privileges: {e}")

# Close superuser cursor and connection
superuser_cursor.close()
superuser_connection.close()

# 4. Connect to the newly created database using the new user
user_connection = psycopg2.connect(
    dbname=new_db_name,
    user=new_user_name,
    password=new_user_password,
    host='localhost'
)
user_connection.autocommit = True

# Create a cursor object using the new user connection
user_cursor = user_connection.cursor()

# 5. Create a new table in the new database
create_table_query = """
CREATE TABLE IF NOT EXISTS credentials (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash BYTEA NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

try:
    user_cursor.execute(create_table_query)
    print(f"Table 'credentials' created successfully in database '{new_db_name}'.")
except Exception as e:
    print(f"Error creating table: {e}")

# Close user cursor and connection
user_cursor.close()
user_connection.close()
