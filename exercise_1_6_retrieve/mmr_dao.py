import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
from pathlib import Path

load_dotenv()

class MMR_DAO:

    def connect(self):
        """
        Establish a connection to the PostgreSQL datatbasw using environment variables.
        return: pyscopg2 connection object or None in case of failure
        """
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("dbname"),
                user=os.getenv("dbuser"),
                password=os.getenv("dbpassword"),
                host=os.getenv("dbhost"),
                port=os.getenv("dbport"),
            )
            return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Error: {error}")

    def insert_file_and_chunks(self, file_path, text_chunks):

        try:
            filename = Path(file_path).name
            suffix = Path(file_path).suffix
            file_ext = suffix.lstrip(".")

            with(open(file_path, "rb") as file_obj):
                file_data = file_obj.read()

            conn = self.connect()
            with conn.cursor() as cursor:
                # Insert the file metadata and content into the complete_files table
                cursor.execute(
                    sql.SQL(
                        "INSERT INTO complete_files(file_name, file_ext, file_data) VALUES (%s, %s, %s) RETURNING pk"
                    ),
                    [filename, file_ext, file_data]
                )
                file_id = cursor.fetchone()[0]
                print(f"THE FILE ID is:{file_id}")

                # Insert the text chunks into the text_chunks table
                for text_chunk in text_chunks:
                    print(f"text chunk is:{text_chunk}")
                    cursor.execute(
                        sql.SQL(
                            "INSERT INTO text_chunks (text, file_id) VALUES (%s, %s)"
                        ),
                        [text_chunk, file_id],
                    )

            conn.commit()
            if conn is not None:
                print("***CONNECTION IS NOT NONE")
            else:
                print("*Connection is NONE*")
            return file_id

        except Exception as e:
            print(f"Error inserting file with chunks: {e}")
        finally:
            if conn:
                conn.close()

    def get_current_text_chunks(self):

        """
        Retrieves all text chunks that have not been vectorized yet.

        Returns:
            dict: A dictionary where keys are primary keys (PKs) and values are text data.
        """
        text_data_dict = {}  # Dictionary to store the retrieved text chunks.
        conn = None  # Connection placeholder.

        try:
            conn = self.connect()  # Establish a database connection.
            with conn.cursor() as cursor:
                # Execute the SQL query to fetch non-vectorized text chunks.
                cursor.execute(
                    """
                    SELECT pk, text
                    FROM text_chunks
                    WHERE is_vectorized = FALSE
                    """
                )

                # Fetch all rows and populate the dictionary with PK and text data.
                rows = cursor.fetchall()
                for row in rows:
                    pk, text_data = row
                    text_data_dict[pk] = text_data

        except Exception as e:
            print(f"Error getting text chunks: {e}")  # Log any exceptions.

        finally:
            if conn:
                conn.close()  # Ensure the connection is closed.

        return text_data_dict  # Return the dictionary of text chunks.

    def store_embeddings(self, embed_dict, chunk_type):
        """
        Stores embeddings into the `mmr_vector` table for a specific chunk type.

        Args:
            embed_dict (dict): A dictionary where keys are chunk IDs and values are their embeddings.
            chunk_type (str): The type of chunk (e.g., "text", "image", or "table").

        Returns:
            list: A list of primary keys (PKs) of the inserted embeddings.
        """
        i = 0  # Counter variable, potentially used for debugging or iterative processes.
        embedded_pks = []  # List to store primary keys of inserted embeddings.
        try:
            conn = self.connect()  # Establish a database connection.
            conn.autocommit = True  # Automatically commit each transaction.

            with conn.cursor() as cursor:
                # Iterate over the embeddings dictionary.
                for k, v in embed_dict.items():
                    while i < 3:  # TODO: Evaluate whether this condition is needed or can be removed.
                        i += 1

                    # Execute an SQL query to insert the embedding and retrieve the new primary key.
                    cursor.execute(
                        sql.SQL(
                            "INSERT INTO mmr_vector (vector, chunk_type, chunk_id) VALUES (%s, %s, %s) RETURNING pk"
                        ),
                        [v, chunk_type, k],
                    )

                    # Fetch and store the returned primary key.
                    embedded_pks.append(cursor.fetchone()[0])

            return embedded_pks  # Return the list of primary keys.

        except Exception as e:
            print(f"Error adding embedding to mmr_vector table: {e}")  # Log any errors.

        finally:
            if conn:
                conn.close()  # Ensure the connection is closed, even if an error occurs.
    
    def update_is_vectorized(self, primary_keys, chunk_type):
        """
        Updates the `is_vectorized` column for specified chunks to True.

        Args:
            primary_keys (list): A list of primary keys (PKs) to update.
            chunk_type (str): The type of the chunks (e.g., "table", "image", "text").
        """
        conn = None  # Connection placeholder.
        try:
            conn = self.connect()  # Establish a database connection.
            conn.autocommit = True  # Automatically commit each transaction.

            table_name = (
                chunk_type + "_chunks"
            )  # Determine the table name based on the chunk type.

            with conn.cursor() as cursor:
                # Iterate over the primary keys to update each chunk individually.
                for key in primary_keys:
                    # Construct and execute the SQL query to update `is_vectorized`.
                    cursor.execute(
                        sql.SQL(
                            "UPDATE {table} SET is_vectorized = True WHERE pk = %s"
                        ).format(table=sql.Identifier(table_name)),
                        [key],  # Use parameterized queries for safety.
                    )

        except Exception as e:
            print(
                f"Error updating is_vectorize in {table_name} table: {e}"
            )  # Log any exceptions.

        finally:
            if conn:
                conn.close()  # Ensure the connection is closed.

    
    def find_similarity(self, vectorized_query, top_k=3):
        conn = None
        try:
            conn = self.connect()  # Establish a database connection.
            #register_vector(conn)  # Register vector support for PostgreSQL.

            with conn.cursor() as cur:
                # Query the top K similar vectors from the `mmr_vector` table.
                cur.execute(
                    sql.SQL(
                        """SELECT pk, chunk_type, chunk_id, 1 - (vector <#> %s::VECTOR) AS similarity
                        FROM mmr_vector
                        ORDER BY similarity DESC
                        LIMIT %s"""
                    ),
                    [vectorized_query, top_k],  
                )

                rows = cur.fetchall()  # Fetch all query results.

                result = []  # List to store the final result.

                # Iterate over the result rows and fetch related data.
                for row in rows:
                    pk, chunk_type, chunk_id, similarity = row

                    # Determine the appropriate table for the chunk type and fetch the file_id.
                    if chunk_type == "image":
                        cur.execute(
                            "SELECT file_id FROM image_chunks WHERE pk = %s", [chunk_id]
                        )
                    elif chunk_type == "table":
                        cur.execute(
                            "SELECT file_id FROM table_chunks WHERE pk = %s", [chunk_id]
                        )
                    else:  # For text chunks.
                        cur.execute(
                            "SELECT file_id FROM text_chunks WHERE pk = %s", [chunk_id]
                        )

                    file_id = cur.fetchone()[0]  # Retrieve the associated file ID.

                    # Fetch the file name from the `complete_files` table.
                    cur.execute(
                        "SELECT file_name FROM complete_files WHERE pk = %s", [file_id]
                    )
                    file_name = cur.fetchone()[0]  # Retrieve the file name.

                    # Append the result with similarity details and file metadata.
                    result.append(
                        {
                            "pk": pk,
                            "chunk_type": chunk_type,
                            "chunk_id": chunk_id,
                            "similarity": similarity,
                            "file_name": file_name,
                        }
                    )

            return result  
        except Exception as e:
            print(f"Error finding similarity: {e}")  # Log any errors.

        finally:
            if conn:
                conn.close()  # Ensure the connection is closed, even if an error occurs.

    def get_chunks_by_id(self, chunk_type, chunk_id):
        """
        Retrieves a chunk's data by its ID and type.

        Args:
            chunk_type (str): The type of the chunk (e.g., "table", "image", "text").
            chunk_id (int): The primary key (PK) of the chunk to retrieve.

        Returns:
            str or bytes: The retrieved chunk data, encoded in base64 if binary.
        """
        conn = None  # Connection placeholder.
        table = chunk_type + "_chunks"  # Determine the table name based on the chunk type.

        # Map chunk type to the appropriate data column name.
        if chunk_type == "table":
            data_type = "table_data"
        elif chunk_type == "image":
            data_type = "image_summary"
        else:
            data_type = chunk_type

        try:
            conn = self.connect()  # Establish a database connection.
            with conn.cursor() as cursor:
                # Construct and execute the SQL query to fetch chunk data by its PK.
                query = f"""
                    SELECT {data_type}
                    FROM {table}
                    WHERE pk = %s
                """
                cursor.execute(query, (chunk_id,))

                # Fetch the retrieved data.
                retrieved_row = cursor.fetchone()[0]

                # Encode binary data as base64 for compatibility.
                if isinstance(retrieved_row, memoryview):
                    retrieved_row = base64.b64encode(retrieved_row).decode("utf-8")

                return retrieved_row  # Return the retrieved chunk data.

        except Exception as e:
            print(f"Error summarizing table chunks: {e}")  # Log any exceptions.

        finally:
            if conn:
                conn.close()  # Ensure the connection is closed.