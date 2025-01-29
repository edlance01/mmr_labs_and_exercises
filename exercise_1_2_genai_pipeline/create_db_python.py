import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Fetch configuration from environment variables
dbname = os.getenv("dbname")  # Database name
user = os.getenv("dbuser")  # Database user
password = os.getenv("dbpassword")  # Database password
host = os.getenv("dbhost")  # Database host
port = os.getenv("dbport")  # Database port


def create_database():
    """
    Create a new PostgreSQL database. If the database already exists,
    catch the error and inform the user.
    """
    try:
        # Connect to the default 'postgres' database to issue the CREATE DATABASE command
        conn = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        )
        # Set isolation level to AUTOCOMMIT to allow database creation
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            # Use SQL identifiers to dynamically create the database name
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        conn.close()  # Close the connection after creating the database
        print("Database created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        # Handle the case where the database already exists
        print("Database already exists.")
    except Exception as e:
        # Handle any other exceptions during database creation
        print(f"Error creating database: {e}")


def create_tables():
    """
    Create the required tables in the database if they do not already exist.
    The tables include `complete_files`, `text_chunks`, `image_chunks`, and `table_chunks`.
    """
    print("Starting create tables ...")
    try:
        # Connect to the newly created database
        with psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        ) as conn:
            with conn.cursor() as cursor:
                # Create the required tables
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS complete_files (
                        pk SERIAL PRIMARY KEY,         -- Unique identifier for files
                        file_name TEXT NOT NULL UNIQUE, -- Unique file name
                        file_ext VARCHAR(10) NOT NULL, -- File extension
                        file_data BYTEA NOT NULL       -- File content stored as binary
                    );

                    CREATE TABLE IF NOT EXISTS text_chunks (
                        pk SERIAL PRIMARY KEY,         -- Unique identifier for text chunks
                        text TEXT NOT NULL,            -- Text content of the chunk
                        text_summary TEXT, -- Summary of the text chunk
                        file_id INTEGER REFERENCES complete_files(pk) ON DELETE CASCADE, 
                                                        -- Foreign key referencing `complete_files`
                        is_vectorized BOOLEAN DEFAULT FALSE -- Indicates if the chunk is vectorized
                    );

                    CREATE TABLE IF NOT EXISTS image_chunks (
                        pk SERIAL PRIMARY KEY,         -- Unique identifier for image chunks
                        image BYTEA NOT NULL,          -- Image content stored as binary
                        image_summary TEXT NOT NULL,   -- Summary or description of the image
                        file_id INTEGER REFERENCES complete_files(pk) ON DELETE CASCADE, 
                                                        -- Foreign key referencing `complete_files`
                        is_vectorized BOOLEAN DEFAULT FALSE -- Indicates if the chunk is vectorized
                    );

                    CREATE TABLE IF NOT EXISTS table_chunks (
                        pk SERIAL PRIMARY KEY,         -- Unique identifier for table chunks
                        table_data TEXT NOT NULL,      -- Table data in serialized format
                        file_id INTEGER REFERENCES complete_files(pk) ON DELETE CASCADE, 
                                                        -- Foreign key referencing `complete_files`
                        is_vectorized BOOLEAN DEFAULT FALSE -- Indicates if the chunk is vectorized
                    );
                    """
                )
            # Inform the user that the tables were created successfully
            print("Tables created successfully.")
    except Exception as e:
        # Handle any errors that occur during table creation
        print(f"Error creating tables: {e}")


# Run the functions to create the database and tables
create_database()  # First, create the database
create_tables()  # Then, create the tables
