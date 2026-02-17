import streamlit as st
from groq import Groq,AuthenticationError, RateLimitError,APIConnectionError,APIError,APITimeoutError


#  POSTAVKE I KLJUČEVI ---
try:
     my_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
     st.error("API ključ nije pronađen")
     st.stop()

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
        "spinner": "Palim digitalnu pećnicu...",
        "download_button":"Preuzmi recept (.txt)",
        "success": "Dobar tek!",
        "warning": "Frižider ti je prazan? Upiši nešto!",
        "footer_text": "Sviđa ti se kuhar? Podrži ga!!!",
        "donate_button": "☕ Kupi mi kavu (Doniraj)",
        "credits":"Made by Filip (20% Digital)",
        "version":"Version 1.0 Stable",
        "ai_prompt":"""
        Ti si iskusni kuhar. Korisnik ima: {namirnice}. Želi: {vrsta_obroka}.
        Napiši točno JEDAN recept na hrvatskom jeziku.
        Format mora biti:
        Naslov:
        Sastojci:
        Priprema:
        Koristi samo standardne kulinarske izraze.
        Ne dodavaj uvod, napomene ni dodatne sekcije.
               
        """ 
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
        "version":"Version 1.0 Stable",
        "ai_prompt":"""
        You are an experienced chef. User has: {namirnice}. Wants: {vrsta_obroka}.
        Write exactly ONE recipe in English.
        Required format:
        Title:
        Ingredients:
        Instructions:
        Use standard culinary terminology only.
        Do not add intro text,notes, or extra sections.
        """
        
        
    }
}

# --- LOGIKA ZA JEZIK (MEMORIJA) ---
if "jezik" not in st.session_state:
    st.session_state.jezik = "EN"

odabrani_jezik = st.radio(
    "Language / Jezik:",
    ("HR", "EN"),
    horizontal=True,
    key="odabrani_jezik",
    index=0 if st.session_state.jezik == "HR" else 1,
)

st.session_state.jezik = odabrani_jezik
# KRATICA: 't' sada sadrži sve tekstove za trenutni jezik
t = TEKSTOVI[st.session_state.jezik]
if "zadnji_recepti" not in st.session_state:
    st.session_state.zadnji_recepti = []


# ---  FUNKCIJA (MOZAK) ---
def generiraj_recept(namirnice, vrsta_obroka, jezik):
    if not my_api_key:
        return "⚠️ Nema API ključa!" if jezik == 'HR' else "⚠️ Missing API Key!"

    try:
        client = Groq(api_key=my_api_key)

        t_local=TEKSTOVI[jezik]
        prompt = t_local["ai_prompt"].format(namirnice=namirnice, vrsta_obroka=vrsta_obroka)
            
        


        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        return chat_completion.choices[0].message.content
    except AuthenticationError as e:
        return "Neispravan API ključ!" if jezik == 'HR' else "Invalid API Key!"
    except RateLimitError as e:
        return "Previše zahtjeva, pričekaj minutu!" if jezik == 'HR' else "Too many requests, wait a minute!"
    except APIConnectionError as e:
        return "Nema interneta ili server nedostupan!" if jezik == 'HR' else "No internet or server unavailable!"
    except APITimeoutError as e:
        return "Zahtjev predugo traje!" if jezik == 'HR' else "Request took too long!"
    except APIError as e:
        return "Problem sa API-jem!" if jezik == 'HR' else "Problem with API!"
        
    except Exception as e:
        st.error(f"Debug: {type(e).__name__}:{e}")
        return "Dogodila se neočekivana greška. Probajte ponovno." if jezik == 'HR' else "An unexpected error occurred. Please try again."
    


#  UI
st.title(t["title"])
st.caption(t["caption"])
st.info(t["instructions"])

st.markdown("---")


col1, col2 = st.columns([2, 1])

with col1:
    namirnice_input = st.text_input(
        t["input_label"],
        placeholder=t["placeholder"],
        key="ingredients_input",
    )

with col2:
    vrsta_obroka = st.selectbox(
        t["meal_label"],
        t["meal_options"],
        key="meal_select",
    )

st.markdown("")
gumb = st.button(t["button"], type="primary", use_container_width=True)
# --- 6. AKCIJA ---
if gumb:
    namirnice_clean = namirnice_input.strip()

    if not namirnice_clean:
        st.warning(t["warning"])
    elif len(namirnice_clean) < 3:
        st.warning("Upiši barem 3 znaka!" if st.session_state.jezik == "HR" else "Type at least 3 characters!")
    elif len(namirnice_clean) > 300:
        st.warning("Unos je predug (max 300 znakova)." if st.session_state.jezik == "HR" else "Input is too long (max 300 characters).")
    else:
        with st.spinner(t["spinner"]):
            recept = generiraj_recept(namirnice_clean, vrsta_obroka, st.session_state.jezik)
            st.session_state.zadnji_recepti.insert(0, recept)
            st.session_state.zadnji_recepti = st.session_state.zadnji_recepti[:5]

            st.markdown("---")
            st.success(t["success"])
            st.text(recept)
            st.download_button(
                label=t["download_button"],
                data=recept,
                file_name="AI_Kuhar_Recept.txt",
                mime="text/plain",
            )

if st.session_state.zadnji_recepti:
    st.markdown("---")
    st.subheader("Zadnji recepti" if st.session_state.jezik == "HR" else "Recent recipes")

    for i, r in enumerate(st.session_state.zadnji_recepti, 1):
        naslov = f"Recept {i}" if st.session_state.jezik == "HR" else f"Recipe {i}"
        with st.expander(naslov):
            st.markdown(r)

    if st.button("Očisti povijest" if st.session_state.jezik == "HR" else "Clear history"):
        st.session_state.zadnji_recepti = []
        st.rerun()
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
    f"""<div style='display: block;text-align: center;width:100%; color: gray; font-size: small;'>{t['credits']} 
    <br>
    <span style="font-size:0.8em;opacity:0.7;">{t["version"]}</span></div>
    """,
    unsafe_allow_html=True
)






