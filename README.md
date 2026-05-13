# Startup Idea Generator

This repository contains a small Python app that generates startup ideas using a LangChain-powered OpenAI chat model and a Streamlit user interface.

## Files

- `startup_agent.py` — command-line version of the idea generator.
- `streamlit_app.py` — Streamlit web interface for generating a startup idea, business name, tagline, and marketing pitch.
- `.env` — local environment file containing `OPENAI_API_KEY`.
- `g/` — additional agent examples and helper scripts.

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install streamlit python-dotenv langchain-openai
```

3. Add your OpenAI API key to `.env`:

```text
OPENAI_API_KEY=your_api_key_here
```

## Run the Streamlit App

From the repository root:

```powershell
streamlit run streamlit_app.py
```

Open the local URL Streamlit prints in your browser.

## Usage

1. Enter an industry (for example, `healthcare`, `education`, or `fintech`).
2. Enter a target audience (for example, `small business owners`, `college students`, or `remote workers`).
3. Click **Generate Startup**.
4. The app will display:
   - Startup idea
   - Business name
   - Tagline
   - Marketing pitch

## Notes

- The app loads `OPENAI_API_KEY` from `.env` so the key is not stored directly in source code.
- If you prefer the command-line version, run:

```powershell
python startup_agent.py
```

- Customize the prompt templates in `streamlit_app.py` to change the generated results.

## Troubleshooting

- If Streamlit fails to start, verify the environment is activated and dependencies are installed.
- If the app reports that `OPENAI_API_KEY` is missing, make sure the `.env` file is in the repository root and contains the key.
