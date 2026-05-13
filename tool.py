from openai import OpenAI

client = OpenAI(api_key="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")

# ---- TOOL 1: Search (Mock or API) ----
def search_tool(query):
    # Replace this with real API (SerpAPI, Tavily, etc.)
    return f"Search results for '{query}': AI is transforming industries like healthcare, finance, and education."

# ---- TOOL 2: Summarizer ----
def summarize_tool(text):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize this in 3 lines:\n{text}"
    )
    return response.output_text

# ---- AGENT ----
def agent(query):
    print("🔍 Searching...")
    search_results = search_tool(query)

    print("🧠 Summarizing...")
    summary = summarize_tool(search_results)

    return summary

# ---- RUN ----
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        output = agent(user_input)
        print("Agent:", output)