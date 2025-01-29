from langchain_openai import OpenAIEmbeddings
from mmr_dao import MMR_DAO
from llm_submission import LLM_Submission


class Retriever:

    def __init__(self):
        self.dao = MMR_DAO()

    def find_similar_vectors(self, query):
        
        openai_embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorized_query = openai_embedding.embed_query(query)
        similar_vectors = self.dao.find_similarity(vectorized_query)

        # print details fo each similar vector 
        for item in similar_vectors:
            print(
                f"Primary Key: {item['pk']} "
                f"Chunk Type: {item['chunk_type']} "
                f"Chunk ID:  {item['chunk_id']} "
                f"Similarity: {item['similarity']} "
                f"File Name: {item['file_name']} "
            )

        return similar_vectors
    
    def run_composite_prompt(self, new_query):
        """
        Executes a process of retrieving similar chunks, fetching their data,
        and submitting a combined prompt to the LLM.

        Args:
            new_query (str): The input text query.

        Returns:
            dict: The result returned by the LLM after processing the composite prompt.
        """
        print("\nRetrieving similar vectors to query.")
        # Step 1: Find similar vectors based on the new query
        ret_similar_vectors = self.find_similar_vectors(new_query)

        # Step 2: Retrieve the data for each similar vector
        retrieved_data = (
            []
        )  # List to store retrieved data and its source file information
        for chunk in ret_similar_vectors:
            # Fetch the actual chunk data using the chunk type and ID
            chunk_data = self.dao.get_chunks_by_id(
                chunk["chunk_type"], chunk["chunk_id"]
            )

            # Append the data and its source file information to the list
            retrieved_data.append(
                {
                    "data": chunk_data,  # The retrieved chunk data
                    "source_file": chunk[
                        "file_name"
                    ],  # The file from which the chunk originated
                }
            )

        # Step 3: Print the retrieved data and their sources for debugging or logging
        for entry in retrieved_data:
            print(f"\nRETURNED DOC: {entry['data']}")
            print(f"\nSOURCE FILE: {entry['source_file']}")
            print("\n***********************************\n")

        # Step 4: Submit the query and retrieved data to the LLM for processing
        llm_submission_result = LLM_Submission().llm_submit(new_query, retrieved_data)

        # Return the result from the LLM submission
        return llm_submission_result
    
   

if __name__ == '__main__':
    query1 = "What is the shortcut to run the current cell and move to the next cell?"
    response1 = Retriever().run_composite_prompt(query1)

    print(f"Response 1: {response1}")