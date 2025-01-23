from langchain_community.document_loaders import UnstructuredWordDocumentLoader

loader = UnstructuredWordDocumentLoader("mmr_test.docx", mode="elements")
documents = loader.load()

for document in documents:
    # Check if the document has a 'source' attribute and if it's a file path
    if (
        hasattr(document, "source")
        and isinstance(document.source, str)
        and document.source.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
    ):
        print("Image found:")
        print(f"  - Source: {document.source}")
        # You can access the raw image data using document.data
    else:
        print("Other element:")
        print(document)
