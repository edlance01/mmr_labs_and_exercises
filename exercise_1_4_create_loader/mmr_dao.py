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
        
