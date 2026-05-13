import os
import requests
from openai import OpenAI

# ==============================
# 🔑 CONFIG
# ==============================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is required.")
if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY environment variable is required.")

client = OpenAI(api_key=OPENAI_API_KEY)

# ==============================
# 🔍 TOOL 1: SEARCH (TAVILY)
# ==============================
def search_tool(query):
    url = "https://api.tavily.com/search"

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "search_depth": "basic",   # or "advanced"
        "max_results": 3
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        # Extract useful content
        results = []
        for r in data.get("results", []):
            results.append(r.get("content", ""))

        return "\n".join(results)

    except Exception as e:
        return f"Search error: {e}"

# ==============================
# 🧠 TOOL 2: SUMMARIZER (OPENAI)
# ==============================
def summarize_tool(text):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
Summarize the following content into 3–5 clear bullet points:

{text}
"""
        )
        return response.output_text

    except Exception as e:
        return f"Summarization error: {e}"

# ==============================
# 🤖 AGENT
# ==============================
def agent(query):
    print("\n🔍 Searching...")
    search_results = search_tool(query)

    if not search_results.strip():
        return "No search results found."

    print("🧠 Summarizing...")
    summary = summarize_tool(search_results)

    return summary

# ==============================
# ▶️ MAIN LOOP
# ==============================
if __name__ == "__main__":
    print("🤖 AI Agent (Search + Summarize)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Agent: Goodbye 👋")
            break

        result = agent(user_input)
        print("\nAgent:\n", result)