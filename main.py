import os
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is required.")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---- TOOL 1: SCRAPER ----
def scrape_tool(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts & styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator=" ")

        # Clean text
        clean_text = " ".join(text.split())

        # Limit size (important for token limits)
        return clean_text[:3000]

    except Exception as e:
        return f"Scraping error: {e}"

# ---- TOOL 2: SUMMARIZER ----
def summarize_tool(text):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize this in 3–5 clear bullet points:\n{text}"
    )
    return response.output_text

# ---- AGENT ----
def agent(url):
    print("🌐 Scraping...")
    scraped_content = scrape_tool(url)

    if "error" in scraped_content.lower():
        return scraped_content

    print("🧠 Summarizing...")
    summary = summarize_tool(scraped_content)

    return summary

# ---- RUN ----
if __name__ == "__main__":
    while True:
        user_input = input("\nEnter URL (or type exit): ")

        if user_input.lower() in ["exit", "quit"]:
            break

        output = agent(user_input)
        print("\nAgent:\n", output)