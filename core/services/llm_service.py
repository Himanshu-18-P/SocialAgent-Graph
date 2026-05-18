import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class LLMService:

    def __init__(self):

        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.4"))

        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature
        )

    def invoke(self, prompt: str):

        response = self.llm.invoke(prompt)

        return response.content

    def invoke_structured(self, prompt: str, schema):

        structured_llm = self.llm.with_structured_output(schema)

        response = structured_llm.invoke(prompt)

        return response