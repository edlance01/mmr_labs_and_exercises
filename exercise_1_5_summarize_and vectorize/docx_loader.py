from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document as DocxDocument
from mmr_dao import MMR_DAO
from summary import TextSummary
from vectorization import Vectorize

class DocxLoader():

    def process_file(self, file_path):

        # //EL TODO check figures image output folder

        doc = DocxDocument(file_path)
        paragraph_chunks = []

        # Extract text content from paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                paragraph_chunks.append(para.text)
        

        # Use RecursiveCharacterTextSplitter to chunk the text
       
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size= 500, chunk_overlap=50
        )

        text_chunks = text_splitter.split_text("\n".join(paragraph_chunks))

        # for chunk in text_chunks_docx:
        #     print(f"\nNew Chunk:{chunk}")

        
        my_con = MMR_DAO().connect()
        if(my_con != None):
            print("db connection is valid")
        
        print(f"About to call dao, file path is:{file_path}, text chunks length is:{len(text_chunks)}") 
        file_id = MMR_DAO().insert_file_and_chunks(file_path, text_chunks)

        print(f"Document Chunks stored in database, file id is:{file_id}") 

        # Summarize
        text_summary_dict = TextSummary().create_summary()

        # Vectorize
        Vectorize().create_and_store_embeddings(text_summary_dict, "text")

        print("Finished, your document has been loaded, chunked, stored in database, summarized, and the summary vectorized and stored in the vector store.")


# Example usage
if __name__ == "__main__":
    docxloader = DocxLoader()
    docxloader.process_file("./Jupyter_Notebook_Info.docx")
