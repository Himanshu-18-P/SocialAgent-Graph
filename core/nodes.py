import json

from core.state import SocialAgentState
from core.prompts import PromptBuilder

from core.services.llm_service import LLMService
from core.services.research_service import ResearchService
from core.schemas import QualityCheckResponse


llm_service = LLMService()
research_service = ResearchService()


class SocialAgentNodes:

    @staticmethod
    def research_node(state: SocialAgentState):

        research = research_service.research_topic(
            topic=state["topic"]
        )

        return {
            "research": research
        }

    @staticmethod
    def evaluation_node(state: SocialAgentState):

        prompt = PromptBuilder.evaluation_prompt(
            topic=state["topic"],
            research_data=state["research"]
        )

        evaluation = llm_service.invoke(prompt)

        return {
            "evaluation": evaluation
        }

    @staticmethod
    def generate_response_node(state: SocialAgentState):

        prompt = PromptBuilder.social_response_prompt(
            topic=state["topic"],
            platform=state["platform"],
            research_data=state["research"],
            evaluation=state["evaluation"]
        )

        social_response = llm_service.invoke(prompt)

        retry_count = state.get("retry_count", 0) + 1

        return {
            "social_response": social_response,
            "retry_count": retry_count
        }

    @staticmethod
    def quality_check_node(state: SocialAgentState):

        prompt = PromptBuilder.quality_check_prompt(
            response=state["social_response"]
        )

        qc = llm_service.invoke_structured(
            prompt=prompt,
            schema=QualityCheckResponse
        )

        return {
            "quality_score": qc.score,
            "approved": qc.approved,
            "final_response": qc.improved_response
        }