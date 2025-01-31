from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from mmr_dao import MMR_DAO  


class TextSummary():
    """
    A class to generate summaries for text data, inheriting from the abstract Summary class.
    """

    def __init__(self) -> None:
        """
        Initialize the TextSummary class.
        Sets up the ChatGPT model and the summarization prompt.
        """
        self.chatgpt = ChatOpenAI(model="gpt-4o", temperature=0)

        self.text_prompt_text = """
        You are an assistant tasked with summarizing text for semantic retrieval.
        These summaries will be embedded and used to retrieve the raw text elements.
        Give a detailed summary of the text below that is well optimized for retrieval.
        Also, provide a one-line description of what the text is about.
        Do not add additional words like Summary: etc.
        Text chunk:
        {element}
        """
        self.text_prompt = ChatPromptTemplate.from_template(self.text_prompt_text)

    def create_summary(self):
        """
        Generate summaries for text chunks stored in the database.

        Retrieves text data, formats it for GPT-4 processing, and stores the results
        in a dictionary for further processing.
        """
        print("\nCreating a text summary.")
        summary_dict = {}

        # Fetch the current text chunks from the database using your text DAO
        text_data = (
            MMR_DAO().get_current_text_chunks()
        )  # Replace with your text DAO method
        
        for chunk_id, text in text_data.items():
            prompt_text = self.text_prompt.format(element=text)
            response = self.chatgpt.invoke([HumanMessage(content=prompt_text)])
            summary = response.content

            summary_dict[chunk_id] = summary

        return summary_dict
