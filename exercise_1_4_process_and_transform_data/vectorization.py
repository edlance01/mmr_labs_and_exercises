import os
import openai
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from mmr_dao import MMR_DAO


class Vectorize:

    def __init__(self):
        self.mmr_dao = MMR_DAO()

    def create_and_store_embeddings(self, sum_dict, chunk_type="text"):
       
        embedding_dict = {}

        for k, v in sum_dict.items():
            embedding_dict[k] = self.get_embedding(v)

        print("storing embedding...")
        self.mmr_dao.store_embeddings(embedding_dict, chunk_type)
        self.mmr_dao.update_is_vectorized(embedding_dict.keys(), chunk_type)

    

    def get_embedding(self, text):
        print("creating embedding ...")
        """
        Generate an embedding for the given text using OpenAI's embeddings API.

        Args:
            text (str): The text to be embedded.

        Returns:
            list[float]: A list of float values representing the embedding vector.
        """
        # Initialize the embedding model
        openai_embedding = OpenAIEmbeddings(model="text-embedding-3-small")

        # Generate the embedding
        content = openai_embedding.embed_query(text)

        # Convert the embedding values to floats (ensures compatibility with storage formats)
        float_content = [float(x) for x in content]

        return float_content
