
[README.md](https://github.com/user-attachments/files/25289533/README.md)
# AI Chef (to-do.py)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/LLM-Groq-111111)](https://groq.com/)

AI Chef is a Streamlit app that generates a recipe from ingredients entered by the user. The app uses the Groq API and the `llama-3.3-70b-versatile` model.

## App Location
- `slike/to-do.py`

## Features
- Enter ingredients from your fridge
- Choose meal type (breakfast/lunch/dinner/dessert or Any)
- Bilingual interface (HR/EN)
- Recipe generation via Groq model
- Download recipe as `.txt`
- Handles common API errors (auth, rate limit, timeout, connection)

## Requirements
- Python 3.10+
- Groq API key

## Installation
If you are in the project root:

```bash
pip install -r requirements.txt
pip install groq
```

Note: if your root `requirements.txt` does not include `groq` yet, add it.

## Set Secret Variable (GROQ_API_KEY)
The app reads the key from `st.secrets["GROQ_API_KEY"]`.

For local development, create this file:
- `.streamlit/secrets.toml`

Content:

```toml
GROQ_API_KEY = "your_real_api_key_here"
```

## Run Locally
From the project root:

```bash
streamlit run slike/to-do.py
```

## Deploy to Streamlit Community Cloud
1. Push the repo to GitHub.
2. Open `https://share.streamlit.io`.
3. Click `New app`.
4. Select repo and branch.
5. Set main file path to `slike/to-do.py`.
6. In app settings, add Secret:
   - key: `GROQ_API_KEY`
   - value: your Groq API key
7. Deploy.

## Security
- Do not commit API keys to source code.
- Use only `st.secrets` for sensitive data.

## Author
- Filip (20% Digital)
