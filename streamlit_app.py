import os
import streamlit as st
from dotenv import load_dotenv

from langgraph_app import run_task

load_dotenv()

st.set_page_config(page_title="LangGraph Agent Workflow", layout="wide")
st.title("LangGraph Agent Workflow")
st.write(
    "Enter a software task and run the LangGraph workflow to generate a plan, research summary, code, test result, and final review."
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error(
        "OPENAI_API_KEY is not set. Add it to your .env file or set the environment variable."
    )
    st.stop()

task = st.text_area(
    "Software Task",
    placeholder="e.g. Build a Python app that summarizes meeting notes from Zoom transcripts",
    height=150,
)

if st.button("Run LangGraph Workflow"):
    if not task.strip():
        st.warning("Please enter a software task before running the workflow.")
    else:
        with st.spinner("Running the LangGraph workflow..."):
            try:
                result = run_task(task)
            except Exception as exc:
                st.error(f"Workflow failed: {exc}")
                result = None

        if result:
            st.success("Workflow completed.")

            st.subheader("🧠 Development Plan")
            st.code(result.get("plan", ""), language="text")

            st.subheader("📚 Research")
            st.code(result.get("research", ""), language="text")

            st.subheader("💻 Generated Code")
            st.code(result.get("code", ""), language="python")

            st.subheader("🧪 Test Result")
            st.code(result.get("test_result", ""), language="text")

            st.subheader("✅ Final Review")
            st.code(result.get("review", ""), language="text")

st.markdown("---")
st.caption("Powered by LangGraph and ChatOpenAI")
