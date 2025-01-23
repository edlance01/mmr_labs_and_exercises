from langchain_community.document_loaders import UnstructuredPDFLoader
import htmltabletomd  # Library to convert HTML tables to Markdown format
import os  # Library for interacting with the operating system


    

# Initialize the PDF loader with specific settings
loader = UnstructuredPDFLoader(
    file_path="Capabilities.pdf",  # Path to the PDF file
    strategy="hi_res",  # High-resolution processing strategy
    extract_images_in_pdf=True,  # Extract images embedded in the PDF
    infer_table_structure=True,  # Detect and parse tables in the PDF
    chunking_strategy="by_title",  # Chunk content by title or section headers
    max_characters=4000,  # Maximum characters per chunk
    new_after_n_chars=4000,  # Create a new chunk after this many characters
    combine_text_under_n_chars=2000,  # Combine small text chunks under this limit
    mode="elements",  # Processing mode (e.g., element-level processing)
    image_output_dir_path="./figures",  # Directory to store extracted images
)

# Load the content of the PDF as a structured dataset
data = loader.load()

# Initialize lists to store text chunks and table chunks
text_chunks = []
table_chunks = []

# Iterate over each extracted element from the PDF
for element in data:
    # Handle table elements and convert them to Markdown if HTML content exists
    if element.metadata["category"] == "Table":
        if "text_as_html" in element.metadata:
            table_markdown = htmltabletomd.convert_table(
                element.metadata["text_as_html"]
            )
            table_chunks.append(
                table_markdown
            )  # Add Markdown table to table_chunks
        else:
            table_chunks.append(
                element.page_content
            )  # Add plain text table content

    # Skip image elements (OCR or otherwise)
    elif element.metadata["category"] == "Image":
        print("\n%%%%Found Image\n")
        print(element.metadata)

    # Process text and composite elements that aren't OCR-generated
    elif (
        element.metadata["category"] == "Text"
        or element.metadata["category"] == "CompositeElement"
    ):
        if (
            "image" in element.page_content.lower()
            or "ocr" in element.page_content.lower()
        ):
            continue  # Skip if the content suggests it's OCR or image-based text
        text_chunks.append(element.page_content)  # Append valid text content

# # Retrieve the names of extracted image files from the figures folder
# image_chunks = os.listdir(os.getenv("IMAGE_OUTPUT_DIR"))

# print("\nYour PDF file has been parsed.  Storing chunks in database . . .")
# # Store the extracted file and its chunks into the database
# file_id = MMR_DAO().store_file_and_chunks(
#     file_path, text_chunks, table_chunks, image_chunks
# )

# print(
#     f"\nPDF file loaded into database, pk in complete_files table is: {file_id}"
# )

# # Vectorize the current chunks for similarity searches
# self.vectorize_current_chunks()

# # Return the database ID of the processed file
# return file_id
