import os
import psycopg2
from psycopg2 import sql
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class PGVectorTable:
    """
    A class to manage PostgreSQL database operations for creating and managing
    the `mmr_vector` table with vector extensions.
    """

    def connect(self):
        """
        Establish a connection to the PostgreSQL database using credentials
        from environment variables.

        Returns:
            conn: A psycopg2 connection object.
        """
        try:
            # Connect to PostgreSQL using environment variables
            conn = psycopg2.connect(
                dbname=os.getenv("dbname"),
                user=os.getenv("dbuser"),
                password=os.getenv("dbpassword"),
                host=os.getenv("dbhost"),
                port=os.getenv("dbport"),
            )
            print("Connected to the PostgreSQL server.")
            return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Error: {error}")

    def create_mmr_vector_table(self):
        """
        Create the `mmr_vector` table in the PostgreSQL database.
        This includes defining a vector column for semantic search.
        """
        try:
            # Connect to the database
            conn = self.connect()
            conn.autocommit = True
            with conn.cursor() as cursor:
                # Drop the table if it exists (for clean initialization)
                cursor.execute("""DROP TABLE IF EXISTS mmr_vector;""")

                # Ensure the `vector` extension is available
                cursor.execute("""CREATE EXTENSION IF NOT EXISTS vector;""")

                # TODO: //EL Limit chunk_type to predefined concrete values
                # Create the `mmr_vector` table with the necessary schema
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS mmr_vector (
                        pk SERIAL PRIMARY KEY,        -- Auto-incrementing primary key
                        vector VECTOR(1536),         -- Vector column for embeddings (1536 dimensions)
                        chunk_type VARCHAR(10) NOT NULL, -- Type of chunk (e.g., text, image)
                        chunk_id INTEGER NOT NULL     -- Foreign key referencing a chunk
                    );
                    """
                )

                # Uncomment the following for additional features like indexing:
                # cursor.execute(
                #     """
                #     CREATE INDEX IF NOT EXISTS mmr_vector_idx
                #     ON mmr_vector
                #     USING ivfflat (vector)
                #     WITH (lists = 100);
                #     """
                # )

                print("mmr_vector table created successfully.")

        except Exception as e:
            print(f"Error creating mmr_vector table: {e}")
        finally:
            # Ensure the connection is closed to avoid resource leaks
            if conn:
                conn.close()


# Instantiate and create the `mmr_vector` table
PGVectorTable().create_mmr_vector_table()
