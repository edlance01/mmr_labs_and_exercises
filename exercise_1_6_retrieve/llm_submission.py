from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class LLM_Submission:

    def __init__(self):
        self.client = ChatOpenAI(model="gpt-4")

    # TODO do we need to check size of all messages before submitting?
    def llm_submit(self, original_query, chunk_data_with_sources):
        print(f"Original Query: {original_query}")
        # context = "\n\n".join([str(doc) for doc in top_docs])
        # Construct the context with source files included
        context = "\n\n".join(
            [
                f"Chunk: {entry['data']}\nSource: {entry['source_file']}"
                for entry in chunk_data_with_sources
            ]
        )

        system_prompt = """You are an assistant for question-answering tasks. Use only 
                the following pieces of retrieved context to answer the 
                question. If the answer is not in the provided context, just say that you 
                don\'t know and do not make up information. Use three sentences maximum and keep the answer concise. Stay strictly within the information provided in the context.
                """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Question: {original_query}\n\nContext: {context}"),
        ]

        # for message in messages:
        #     print(f"Role: {message['role']}")
        #     print(f"Content: {message['content']}\n")
        # NOTE - if prompt size or chunk size change or LLM factors...we will need to check this before invoke
        response = self.client.invoke(messages)

        final_answer = f"{response.content}\n\nSources: " + ", ".join(
            sorted(set(f"{entry['source_file']}" for entry in chunk_data_with_sources))
        )

        return final_answer
        # print(response.content)

        # return response.content
