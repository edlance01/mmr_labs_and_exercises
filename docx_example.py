import os
from docx import Document as DocxDocument
from langchain.text_splitter import CharacterTextSplitter

docx_file_path = "mmr_test.docx"
doc = DocxDocument(docx_file_path)

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
output_folder = "image_output_folder"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

all_chunks = []
for rel in doc.part.rels.values():
    if "image" in rel.target_ref:
        image = rel.target_part.blob
        image_extension = rel.target_ref.split(".")[-1]
        image_name = f"image_{rel.rId}.{image_extension}"
        image_path = os.path.join(output_folder, image_name)

        with open(image_path, "wb") as img_file:
            img_file.write(image)
            print(f"Saved: {image_path}")



# for table in doc.tables:

#     table_text = ""
#     for row in table.rows:
#         row_text = " | ".join(cell.text for cell in row.cells)
#         table_text += row_text + "\n"

#     # Split the table text into chunks
#     table_chunks = text_splitter.split_text(table_text)
#     all_chunks.extend(table_chunks)

# # Now you have all_chunks, which contains the table chunks and any other text chunks
# for chunk in all_chunks:
#     print("\n*****NEW TABLE*****\n")
#     print(chunk)
