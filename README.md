[README.md](https://github.com/user-attachments/files/25364260/README.md)
# AI Chef

A Streamlit app that generates a recipe from user-provided ingredients using Groq (`llama-3.3-70b-versatile`).

## Features
- Bilingual UI (Croatian/English)
- Generates exactly one recipe per request
- Structured output: title, ingredients, instructions, and approximate nutrition
- Input validation (empty input, min/max length)
- Recent recipe history with clear option
- Download recipe as `.txt`

## Requirements
- Python 3.10+
- A Groq API key

## Installation
```bash
pip install streamlit groq
```

## API Key Setup
Add this to Streamlit secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

## Run the App
From the project root:

```bash
streamlit run Perplex/slike/en-hr_chef.py
```

## Main File
- `Perplex/slike/en-hr_chef.py` - main app

## Notes
- Nutrition values are AI-generated estimates and not a substitute for professional dietary analysis.
- The app requires a valid Groq API key in `st.secrets`.

#Author
Filip (20% Digital)
