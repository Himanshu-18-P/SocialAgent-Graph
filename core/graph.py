from langgraph.graph import StateGraph, START, END

from core.state import SocialAgentState
from core.nodes import SocialAgentNodes


def route_quality(state: SocialAgentState):
    if state["quality_score"] < 8 and state.get("retry_count", 0) < 3:
        return "retry"

    return "stop"


builder = StateGraph(SocialAgentState)

builder.add_node("research", SocialAgentNodes.research_node)
builder.add_node("evaluation", SocialAgentNodes.evaluation_node)
builder.add_node("generate_response", SocialAgentNodes.generate_response_node)
builder.add_node("quality_check", SocialAgentNodes.quality_check_node)

builder.add_edge(START, "research")
builder.add_edge("research", "evaluation")
builder.add_edge("evaluation", "generate_response")
builder.add_edge("generate_response", "quality_check")

builder.add_conditional_edges(
    "quality_check",
    route_quality,
    {
        "retry": "generate_response",
        "stop": END
    }
)

graph = builder.compile()