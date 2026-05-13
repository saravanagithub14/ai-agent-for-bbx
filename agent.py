import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is required.")

client = OpenAI(api_key=OPENAI_API_KEY)

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Bye 👋")
        break

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=user_input
    )

    print("Bot:", response.output_text)