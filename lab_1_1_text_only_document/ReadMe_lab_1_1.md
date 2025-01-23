
Part One:
1. Create a class DocxLoader, create a method named process_file that takes a file_path.
2. Following the examples provided in the notebook (lamo.ipynb), use Python docx to parse the text from the provided document (acme_bank_consolidated_performance_report.docx)
3. For now, only worry about text, not images or tables.
4. Split the parsed paragraphs into chunks of 500, with a chunk overlap of 50.
5. Print out a few values to ensure your list of chunks is being populated.

Part Two
6. Create a class MMR_Dao
7. Write functionality to:
    A. Insert the file_name, file_data, and file_ext into the complete_files table.
    B. Insert the file the text of each chunk, and file_id into the text_chunks table.
8. Still in MMR_Dao, create a method to pull every row where the is_vectorized column = False (should be all of our records at this point).
    A. Populate a dictionary with the primary key and value of each text chunk.
9. Write a simple function to view a few text_chunks to get a feel for what they look like and validate things are working as they should.

Part Three
10. Create a Vectorization class
11. Embed each chunk (remember, you may have to convert them to floats for storing)
12. Store each chunk in the mmr_vector table.
13. Embed each of them and store them in the mmr_vector table.  Remember to store the vector, the chunk type ('text' in this case), and the chunk_id (which is the primary key from the text_chunks table).


Part Four
14. 
