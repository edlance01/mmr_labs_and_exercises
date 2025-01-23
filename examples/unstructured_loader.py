from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredWordDocumentLoader


# Step 1: Load the .docx file
#loader = UnstructuredWordDocumentLoader("acme_bank_consolidate_performance_report.docx", mode="elements")
loader = UnstructuredWordDocumentLoader("mmr_test.docx", mode="elements")

# Step 2: Load and split documents (if necessary)
documents = loader.load()
print(f"LEN is:{len(documents)}")
print(f"KEYS:{documents[0].metadata.keys()}")
# Step 3: Process content to identify tables
for idx, doc in enumerate(documents):
    content = doc.page_content
    metadata = doc.metadata
    print(f"\nCONTENT:{content}")
    print(f"\nmetadata\n:{metadata}")
    # print(f"Category:{metadata.get("category")}")
   #print(f"\nMetaData:\n{metadata}")
    # if 'text_as_html' in metadata:
    #     print("\nNEW TABLE:\n")
    #     print(metadata['text_as_html'])

    
 
