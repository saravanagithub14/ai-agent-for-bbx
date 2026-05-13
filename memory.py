import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os
from groq import Groq

# -----------------------------
# CONFIG
# -----------------------------

st.set_page_config(page_title="AI Web Agent (Groq)", layout="centered")

# Use environment variable for your Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is required.")

client = Groq(api_key=GROQ_API_KEY)

MEMORY_FILE = "memory.json"
MODEL = "llama-3.1-8b-instant"  # Fast Groq model; alternatives: llama-3.3-70b-versatile

# -----------------------------
# MEMORY FUNCTIONS
# -----------------------------

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"history": []}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


memory = load_memory()

# -----------------------------
# SCRAPER
# -----------------------------

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text[:3000]  # limit for demo
    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# SUMMARIZER (Groq)
# -----------------------------

def summarize(text):
    prompt = f"Summarize this content in simple terms:\n\n{text}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.5,
    )

    return response.choices[0].message.content

# -----------------------------
# CHAT AGENT (Groq)
# -----------------------------

def chat_with_memory(query):
    past_data = memory["history"][-3:]  # last 3 summaries

    context = ""
    for item in past_data:
        context += f"URL: {item['url']}\nSummary: {item['summary']}\n\n"

    system_prompt = (
        "You are an AI assistant. Use the knowledge below to answer the user's question. "
        "If the answer is not present in the knowledge, say: 'I don't know based on stored data.'\n\n"
        f"Previously collected knowledge:\n{context}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        max_tokens=512,
        temperature=0.5,
    )

    return response.choices[0].message.content

# -----------------------------
# UI
# -----------------------------

st.title("🌐 Agent - Web Scraper & Summarizer with Memory")
st.caption(f"Powered by Groq · Model: `{MODEL}`")

# -------- Scraping Section --------
st.subheader("🔍 Scrape & Summarize")

url = st.text_input("Enter website URL")

if st.button("Scrape & Summarize"):
    if url:
        with st.spinner("🔄 Scraping website..."):
            content = scrape_website(url)

        if content.startswith("Error:"):
            st.error(content)
        else:
            with st.spinner("🧠 Summarizing with Groq..."):
                summary = summarize(content)

            st.subheader("📄 Summary")
            st.write(summary)

            # Save to memory
            memory["history"].append({
                "url": url,
                "summary": summary
            })
            save_memory(memory)
            st.success("✅ Summary saved to memory!")
    else:
        st.warning("Please enter a URL.")

# -------- Memory Display --------
st.subheader("📜 Past Summaries")

if memory["history"]:
    for item in reversed(memory["history"][-5:]):
        with st.expander(f"🔗 {item['url']}"):
            st.write(item["summary"])
else:
    st.write("No memory yet.")

# -------- Chat Section --------
st.subheader("💬 Chat with Scraped Data")

user_query = st.text_input("Ask something based on stored summaries")

if st.button("Ask AI"):
    if user_query:
        with st.spinner("🤖 Thinking..."):
            answer = chat_with_memory(user_query)
        st.info(f"🤖 {answer}")
    else:
        st.warning("Please enter a question.")

# -------- Sidebar Controls --------
st.sidebar.header("⚙️ Controls")
st.sidebar.markdown(f"**Model:** `{MODEL}`")
st.sidebar.markdown("**Change model** by editing the `MODEL` variable in `memory.py`")
st.sidebar.markdown("Available Groq models:\n- `llama-3.1-8b-instant` (fast)\n- `llama-3.3-70b-versatile` (smarter)\n- `qwen/qwen3-32b`")

if st.sidebar.button("🗑️ Clear Memory"):
    memory["history"] = []
    save_memory(memory)
    st.sidebar.success("Memory cleared!")