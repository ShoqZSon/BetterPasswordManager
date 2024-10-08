import psycopg2
from psycopg2 import sql

class DatabasePSQL:
    def __init__(self,user,password,database):
        self.__cursor = None
        self.__connection = None

        self.__admin_dbname = 'postgres'
        self.__admin_user = 'postgres'
        self.__admin_password = 'admin'
        self.__host = '192.168.56.111'

        self.__newUser = user
        self.__newPassword = password
        self.__newDB = database

        self.__currentUser = None

    def connect(self, db, user, password):
        try:
            self.__connection = psycopg2.connect(
                dbname=db,
                user=user,
                password=password,
                host=self.__host
            )
            self.__currentUser = user
            self.__connection.autocommit = True
            self.__cursor = self.__connection.cursor()
            print(f"Connected to the database '{db}' successfully.")

            return True
        except psycopg2.OperationalError as e:
            print(f"Failed to connect to the database: {e}")
            return False

    def createDB(self):
        # 1. Create a new database
        try:
            self.__cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.__newDB))
            )
            print(f"Database '{self.__newDB}' created successfully.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{self.__newDB}' already exists.")

    def createUser(self):
        # 2. Create a new user with a password
        try:
            self.__cursor.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(self.__newUser)),
                [self.__newPassword]
            )
            print(f"User '{self.__newUser}' created successfully.")
        except psycopg2.errors.DuplicateObject:
            print(f"User '{self.__newUser}' already exists.")

    def grantPrivileges(self):
        # 3. Grant privileges to the new user on the new database
        try:
            self.__cursor.execute(
                sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                    sql.Identifier(self.__newDB), sql.Identifier(self.__newUser)
                )
            )
            print(f"Privileges granted to user '{self.__newUser}' on database '{self.__newDB}'.")
        except Exception as e:
            print(f"Error granting privileges: {e}")

    def disconnect(self):
        # Close superuser cursor and connection
        self.__cursor.close()
        self.__connection.close()

    def createPasswordsTable(self):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS Passwords ("
                                     "id SERIAL PRIMARY KEY,"
                                     "password_hash BYTEA NOT NULL,"
                                     "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                                     ");")
        try:
            self.__cursor.execute(query)
            print(f"Table 'Passwords' created successfully in database '{self.__newDB}'.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def createEntryPWTable(self,password_hash: bytes):
        # SQL query to insert data into the Passwords table
        query = sql.SQL("INSERT INTO Passwords (password_hash) VALUES (%s)")

        try:
            # Execute the SQL query with the provided values
            self.__cursor.execute(query, (password_hash,))
            print(f"Entry for user '{self.__newUser}' created successfully.")
        except Exception as e:
            print(f"Error creating entry: {e}")

    def retrievePassword(self):
            """
            Retrieves the first password in the tabel (for now).
            :return: The encrypted password in bytes.
            """
            query = sql.SQL("SELECT password_hash FROM Passwords LIMIT 1;")  # Assuming you only need one key

            try:
                self.__cursor.execute(query)
                result = self.__cursor.fetchone()
                if result:
                    return bytes(result[0])  # Assuming the key is in the first column
                else:
                    raise ValueError("No key found in the database.")
            except Exception as e:
                print(f"Error retrieving key: {e}")
                raise  # Re-raise the exception to handle it at a higher level

    def createKeysTable(self):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS Keys ("
                        "id SERIAL PRIMARY KEY,"
                        "key_type TEXT NOT NULL DEFAULT 'en-/decryption',"
                        "key BYTEA UNIQUE NOT NULL,"
                        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                        "created_by TEXT NOT NULL);")

        try:
            self.__cursor.execute(query)
            print(f"Table 'Keys' created successfully in database '{self.__newDB}'.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def retrieveKey(self):
        """
        Retrieves the encryption key from the database.
        :return: Encryption key (bytes).
        """
        query = sql.SQL("SELECT key FROM Keys LIMIT 1;")  # Assuming you only need one key

        try:
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            if result:
                return bytes(result[0])  # Assuming the key is in the first column
            else:
                raise ValueError("No key found in the database.")
        except Exception as e:
            print(f"Error retrieving key: {e}")
            raise  # Re-raise the exception to handle it at a higher level

    def createEntryKeysTable(self,key: bytes):
        # SQL query to insert data into the Passwords table
        query = sql.SQL("INSERT INTO Keys (key_type,key,created_by) VALUES (%s,%s,%s)")

        try:
            # Execute the SQL query with the provided values
            self.__cursor.execute(query, ('en-/decryption',key,self.get_current_user()))
            print(f"Entry for user '{self.__newUser}' created successfully.")
        except Exception as e:
            print(f"Error creating entry: {e}")

    # Getter methods
    def get_admin_dbname(self):
        return self.__admin_dbname

    def get_admin_user(self):
        return self.__admin_user

    def get_admin_password(self):
        return self.__admin_password

    def get_host(self):
        return self.__host

    def get_new_user(self):
        return self.__newUser

    def get_new_password(self):
        return self.__newPassword

    def get_new_db(self):
        return self.__newDB

    def get_current_user(self):
        return self.__currentUser