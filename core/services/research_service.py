import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


class ResearchService:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")

        if not self.api_key:
            raise ValueError("Missing TAVILY_API_KEY in .env")

        self.client = TavilyClient(api_key=self.api_key)

    def research_topic(self, topic: str, max_results: int = 5):
        results = self.client.search(
            query=topic,
            search_depth="advanced",
            max_results=max_results
        )

        research_data = []

        for item in results.get("results", []):
            research_data.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content")
            })

        return research_data