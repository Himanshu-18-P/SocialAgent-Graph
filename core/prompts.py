import json


class PromptBuilder:

    @staticmethod
    def evaluation_prompt(topic: str, research_data: list) -> str:
        research_text = json.dumps(research_data, indent=2)

        return f"""
Evaluate this research.

Topic:
{topic}

Research:
{research_text}

Check:
- Is it relevant?
- What are the key useful points?
- What is missing?
- What should we be careful not to overclaim?

Return concise notes.
"""

    @staticmethod
    def social_response_prompt(
        topic: str,
        platform: str,
        research_data: list,
        evaluation: str
    ) -> str:
        research_text = json.dumps(research_data, indent=2)

        return f"""
Write a helpful {platform} response.

Topic:
{topic}

Research:
{research_text}

Evaluation:
{evaluation}

Rules:
- Sound natural, like a real user.
- Be helpful and specific.
- Do not sound promotional.
- Do not overclaim.
- Mention practical steps.
- Keep under 250 words.
"""

    @staticmethod
    def quality_check_prompt(response: str) -> str:
        return f"""
You are a strict senior social media reviewer.

Review this response and score it from 1 to 10.

Scoring:
- 9-10 = excellent, ready to post
- 7-8 = good, minor edits needed
- 5-6 = average, needs improvement
- 1-4 = poor, do not post

Rules:
- approved must be true only if score >= 8
- approved must be false if score < 8
- score must be an integer from 1 to 10

Response:
{response}

Return ONLY valid JSON:

{{
  "score": 8,
  "approved": true,
  "issues": ["issue 1"],
  "improved_response": "final improved version"
}}
"""