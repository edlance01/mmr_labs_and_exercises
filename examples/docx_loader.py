from docx import Document as DocxDocument
from langchain.text_splitter import CharacterTextSplitter

docx_file_path = "mmr_test.docx"
doc = DocxDocument(docx_file_path)

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

all_chunks = []
for table in doc.tables:
  
    table_text = ""
    for row in table.rows:
        row_text = " | ".join(cell.text for cell in row.cells)
        table_text += row_text + "\n"

    # Split the table text into chunks
    table_chunks = text_splitter.split_text(table_text)
    all_chunks.extend(table_chunks)

# Now you have all_chunks, which contains the table chunks and any other text chunks
for chunk in all_chunks:
    print("\n*****NEW TABLE*****\n")
    print(chunk)
