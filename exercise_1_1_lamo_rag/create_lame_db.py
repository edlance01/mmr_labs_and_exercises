import psycopg2
from psycopg2 import sql


def create_database(db_name, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # Connect to the default database
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created successfully.")
            #cur.execute(sql.SQL("CREATE EXTENSION pgvector;"))
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")


def create_tables(db_name, user, password, host, port):
    try:
        with psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS text_chunks (
                        id SERIAL PRIMARY KEY,
                        text TEXT NOT NULL,
                        is_vectorized BOOLEAN DEFAULT FALSE -- Indicates if the chunk is vectorized
                    );

                    CREATE TABLE IF NOT EXISTS mmr_vector (
                        id SERIAL PRIMARY KEY,
                        vector VECTOR(1536),
                        text_chunk_id INTEGER REFERENCES text_chunks(id)
                    );
                """
                )
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")


# Replace with your actual database credentials
db_name = "lame_db"
user = "postgres"
password = "admin"
host = "localhost"
port = "5432"

create_database(db_name, user, password, host, port)
create_tables(db_name, user, password, host, port)
