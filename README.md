# SocialAgent-Graph

A LangGraph-powered agent that researches a topic, drafts a social media response, runs an automated quality check with a retry loop, and posts the final response to Reddit. Comes with a Streamlit UI for review and editing before publishing.

## How it works

The graph runs four nodes in sequence with a conditional retry on quality:

```
START → research → evaluation → generate_response → quality_check ─┬─ retry → generate_response
                                                                   └─ stop  → END
```

- **research** — Tavily web search collects sources for the topic.
- **evaluation** — LLM extracts key useful points, gaps, and caveats from the research.
- **generate_response** — LLM drafts a natural, non-promotional response for the target platform.
- **quality_check** — LLM scores the draft 1–10 against a strict rubric (Pydantic-validated). If score `< 8` and retries `< 3`, loop back; otherwise finish.

The final response is shown in Streamlit for manual edits, then routed through `SocialRouter` to the platform adapter (currently Reddit via PRAW).

## Project layout

```
core/
  graph.py                 # LangGraph wiring + retry routing
  nodes.py                 # research / evaluation / generate / quality_check nodes
  state.py                 # SocialAgentState TypedDict
  schemas.py               # Pydantic schema for quality check output
  prompts.py               # PromptBuilder for each node
  services/
    llm_service.py         # ChatOpenAI wrapper (.invoke / .invoke_structured)
    research_service.py    # Tavily search client
    social_router.py       # Dispatches to the right platform
  platforms/
    reddit.py              # PRAW-based Reddit posting
main.py                    # Streamlit app
requirements.txt
```

## Setup

1. Create and activate a virtual environment, then install dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4.1-mini
   OPENAI_TEMPERATURE=0.4

   TAVILY_API_KEY=tvly-...

   REDDIT_CLIENT_ID=...
   REDDIT_CLIENT_SECRET=...
   REDDIT_USERNAME=...
   REDDIT_PASSWORD=...
   REDDIT_USER_AGENT=SocialAgent-Graph/0.1 by <your-username>
   ```

## Run

```powershell
streamlit run main.py
```

Then in the UI:

1. Enter a topic and pick a subreddit.
2. Click **Generate Response** — the graph runs research → evaluation → draft → quality check (with up to 3 retries).
3. Review the quality score, edit the final response if needed.
4. Click **Post to Reddit** to publish.

## Extending to new platforms

Add a new adapter under [core/platforms/](core/platforms/) exposing a `create_post`-style method, then route to it from [core/services/social_router.py](core/services/social_router.py) and add the option to the `platform` selectbox in [main.py](main.py).

## Tech stack

LangGraph · LangChain · OpenAI · Tavily · PRAW · Streamlit · Pydantic
