import streamlit as st
from groq import Groq
import os

#  POSTAVKE I KLJUČEVI ---
my_api_key = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="AI Kuhar")


#  RJEČNIK S TEKSTOVIMA (Sve na jednom mjestu) ---
TEKSTOVI = {
    "HR": {
        "title": "AI Kuhar",
        "caption": "Pokreće Groq (Llama 3.3)",
        "instructions":"Upišite namirnice koje imate kod kuće (odvoji zarezom), odaberite vrstu jela i AI će ti smisliti recept!",
        "language_label": "Jezik / Language:",
        "input_label": "Što imaš u frižideru?",
        "placeholder": "npr. jaja, špek, luk",
        "meal_label": "Koji obrok želiš?",
        "meal_options": ["Svejedno", "Doručak", "Ručak", "Večera", "Desert"],
        "button": "Generiraj recept",
        "spinner": "Palim digitalnu pečnicu...",
        "download_button":"Preuzmi recept (.txt)",
        "success": "Dobar tek!",
        "warning": "Frižider ti je prazan? Upiši nešto!",
        "footer_text": "Sviđa ti se kuhar? Podrži ga!!!",
        "donate_button": "☕ Kupi mi kavu (Doniraj)",
        "credits":"Made by Filip (20% Digital)",
        "version":"Version 0.9 beta"
    },
    "EN": {
        "title": "The AI Chef",
        "caption": "Powered by Groq (Llama 3.3)",
        "instructions": "Enter ingredients you have at home (separated by commas), choose a meal type, and let AI create a recipe for you!",
        "language_label": "Language / Jezik:",
        "input_label": "What's in your fridge?",
        "placeholder": "e.g. eggs, bacon, onion",
        "meal_label": "Which meal?",
        "meal_options": ["Any", "Breakfast", "Lunch", "Dinner", "Dessert"],
        "button": "Generate Recipe",
        "spinner": "Cooking up magic...",
        "download_button":"Download Recipe (.txt)",
        "success": "Bon appétit!",
        "warning": "Fridge empty? Type something!",
        "footer_text": "Like the Chef? Support him!",
        "donate_button": "☕ Buy me a coffee (Donate)",
        "credits":"Made by Filip (20% Digital)",
        "version":"Version 0.9 beta"
    }
}

# --- LOGIKA ZA JEZIK (MEMORIJA) ---
if 'jezik' not in st.session_state:
    st.session_state.jezik = 'EN' # Početni jezik

# Radio gumb na vrhu
odabrani_jezik = st.radio(
    TEKSTOVI[st.session_state.jezik]["language_label"],
    ('HR', 'EN'),
    horizontal=True,
    index=0 if st.session_state.jezik == 'HR' else 1
)

# Ako se promijeni jezik, osvježi stranicu
if odabrani_jezik != st.session_state.jezik:
    st.session_state.jezik = odabrani_jezik
    st.rerun()

# KRATICA: 't' sada sadrži sve tekstove za trenutni jezik
t = TEKSTOVI[st.session_state.jezik]


# ---  FUNKCIJA (MOZAK) ---
def generiraj_recept(namirnice, vrsta_obroka, jezik):
    if not my_api_key:
        return "⚠️ Nema API ključa!" if jezik == 'HR' else "⚠️ Missing API Key!"
    
    try:
        client = Groq(api_key=my_api_key)
        
        # Prilagođavamo prompt ovisno o jeziku
        if jezik == 'HR':
            prompt = f"""
            Ti si iskusni kuhar. Korisnik ima: {namirnice}. Želi: {vrsta_obroka}.
            Zadatak: Napravi JEDAN recept na hrvatskom jeziku.
            Struktura: Naslov, Sastojci, Priprema. Ne izmišljaj riječi.
            """
        else:
            prompt = f"""
            You are an experienced chef. User has: {namirnice}. Wants: {vrsta_obroka}.
            Task: Create ONE recipe in English.
            Structure: Title, Ingredients, Instructions. Use standard terminology.
            """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"


#  PRIKAZ SUČELJA (UI) 
st.title(t["title"])
st.caption(t["caption"])
st.info(t["instructions"])

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    namirnice_input = st.text_input(t["input_label"], placeholder=t["placeholder"])

with col2:
    vrsta_obroka = st.selectbox(t["meal_label"], t["meal_options"])

st.markdown("")
gumb = st.button(t["button"], type="primary", use_container_width=True)

# --- 6. AKCIJA ---
if gumb:
    if namirnice_input:
        with st.spinner(t["spinner"]):
            # Šaljemo i jezik u funkciju!
            recept = generiraj_recept(namirnice_input, vrsta_obroka, st.session_state.jezik)
            
            st.markdown("---")
            st.success(t["success"])
            st.markdown(recept)
            st.download_button(
                label=t["download_button"],
                data=recept,
                file_name="AI_Kuhar_Recept.txt",
                mime="text/plain"
            )
    else:
        st.warning(t["warning"])

# --- FOOTER (DONACIJE) ---
st.write("")
st.write("")
st.write("")
st.write("")
st.markdown("-----")

paypal_url = "https://paypal.me/filipvz"
col_l, col_s, col_d = st.columns([1, 2, 1])

with col_s:
    st.write(t["footer_text"])
    st.link_button(t["donate_button"], url=paypal_url)
#--- POTPIS AUTORA i Verzija ---
st.write("") 
st.markdown(
    f"""<div style='display: block;text-align: center;width:100%: color: gray; font-size: small;'>{t['credits']} 
    <br>
    <span style="font-size:0.8em;opacity:0.7;">{t["version"]}</span></div>
    """,
    unsafe_allow_html=True
)


