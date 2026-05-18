import streamlit as st
from dotenv import load_dotenv

from core.graph import graph
from core.services.social_router import SocialRouter

load_dotenv()

st.set_page_config(
    page_title="SocialAgent Graph",
    page_icon="🤖",
    layout="centered"
)

st.title("SocialAgent Graph")
st.write("Generate, review, edit, and post social media responses.")

topic = st.text_area(
    "Topic",
    value="best way to learn LangGraph for production AI agents"
)

platform = st.selectbox(
    "Platform",
    ["reddit"]
)

subreddit = st.text_input(
    "Subreddit",
    value="test"
)

if st.button("Generate Response"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Researching and generating response..."):
            result = graph.invoke({
                "topic": topic,
                "platform": platform,
                "retry_count": 0
            })

        st.session_state["agent_result"] = result
        st.session_state["edited_response"] = result.get("final_response", "")

if "agent_result" in st.session_state:
    result = st.session_state["agent_result"]

    st.subheader("Quality Check")
    st.write("Score:", result.get("quality_score"))
    st.write("AI Approved:", result.get("approved"))
    st.write("Retries:", result.get("retry_count"))

    st.subheader("Edit Before Posting")

    edited_response = st.text_area(
        "Final response",
        value=st.session_state.get("edited_response", ""),
        height=350
    )

    st.session_state["edited_response"] = edited_response

    st.subheader("Post")

    if st.button("Post to Reddit"):
        if not edited_response.strip():
            st.error("Response is empty.")
        else:
            with st.spinner("Posting to Reddit..."):
                upload_result = SocialRouter.upload(
                    platform=platform,
                    title=f"AI Discussion: {topic[:180]}",
                    body=edited_response,
                    subreddit=subreddit
                )

            if upload_result.get("posted"):
                st.success("Posted successfully.")
                st.markdown(f"[Open Reddit Post]({upload_result.get('posted_url')})")
            else:
                st.error("Posting failed.")
                st.write(upload_result)