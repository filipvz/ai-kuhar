# 👨‍🍳 AI Chef / AI Kuhar

A bilingual Streamlit app that generates recipes from user-provided ingredients using Groq (`llama-3.3-70b-versatile`).

## Features
- Bilingual UI (Croatian / English)
- Real-time streaming recipe generation
- Structured output: title, ingredients, instructions, and approximate nutrition info
- Input validation (empty input, min/max length)
- Recipe rating (1–5 stars)
- Download recipe as `.txt`

## Requirements
- Python 3.10+
- A Groq API key

## Installation
```bash
pip install streamlit groq
```

## API Key Setup
Add this to Streamlit secrets (`.streamlit/secrets.toml`):

```toml
GROQ_API_KEY = "your_groq_api_key"
```

## Run the App
```bash
streamlit run to-do.py
```

## Notes
- Nutrition values are AI-generated estimates and not a substitute for professional dietary advice.
- Requires a valid Groq API key in `st.secrets`.

## Author
Filip (20% Digital)
