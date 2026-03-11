import streamlit as st
from groq import Groq,AuthenticationError, RateLimitError,APIConnectionError,APIError,APITimeoutError
import gspread
from google.oauth2.service_account import Credentials

def spoji_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("AI Kuhar Ocjene").sheet1
    return sheet



#  POSTAVKE I KLJUČEVI ---
try:
     my_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
     st.error("API ključ nije pronađeni")
     st.stop()

st.set_page_config(page_title="AI Kuhar",page_icon="👨‍🍳")


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
        "version":"Version 0.9 beta",
        "ai_prompt":"""
        Ti si iskusni kuhar. Korisnik ima: {namirnice}. Želi: {vrsta_obroka}.
        Napiši točno JEDAN recept na hrvatskom jeziku.
        Format mora biti:

        Naslov:

        Sastojci:

        Priprema:

        Nutritivne informacije (okvirno po porciji):
        -Kalorije:
        -Proteini:
        -Ugljeni hidrati:
        -Masti:

        Ako procjena nije sigurna, napiši da je okvirna.
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
        "version":"Version 0.9 beta",
        "ai_prompt":"""
        You are an experienced chef. User has: {namirnice}. Wants: {vrsta_obroka}.
        Write exactly ONE recipe in English.
        Required format:

        Title:

        Ingredients:

        Instructions:

        Nutritional information (per serving):
        -Calories:
        -Proteins:
        -Carbs:
        -Fats:
        
        If uncertain, clearly state it is an estimate.
        Use standard culinary terminology only.
        Do not add intro text, notes, or extra sections.
        """

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
       yield "⚠️ Nema API ključa!" if jezik == 'HR' else "⚠️ Missing API Key!"
       return
    try:
        client = Groq(api_key=my_api_key)

        t_local=TEKSTOVI[jezik]
        prompt = t_local["ai_prompt"].format(namirnice=namirnice, vrsta_obroka=vrsta_obroka)    
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            stream=True 
        )
        for chunk in chat_completion:
            tekst=chunk.choices[0].delta.content
            if tekst is not None:
                yield tekst
    except AuthenticationError as e:
        yield "Neispravan API ključ!" if jezik == 'HR' else "Invalid API Key!"
        return
    except RateLimitError as e:
        yield "Previše zahtjeva, pričekaj minutu!" if jezik == 'HR' else "Too many requests, wait a minute!"
        return
    except APIConnectionError as e:
        yield "Nema interneta ili server nedostupan!" if jezik == 'HR' else "No internet or server unavailable!"
        return
    except APITimeoutError as e:
        yield "Zahtjev predugo traje!" if jezik == 'HR' else "Request took too long!"
        return
    except APIError as e:
        yield "Problem sa API-jem!" if jezik == 'HR' else "Problem with API!"
        return
    except Exception as e:
        yield f"Error: {str(e)}"
        return

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
    namirnice_clean = namirnice_input.strip()
    st.session_state.namirnice_clean = namirnice_clean
    if namirnice_clean:
        st.session_state.pop("recipe_rating", None)
    if not namirnice_clean:
        st.session_state.trenutni_recept = None
        st.warning(t["warning"])
    elif len(namirnice_clean) < 3:
        st.warning("Upiši barem 3 znaka!" if st.session_state.jezik == "HR" else "Type at least 3 characters!")
    elif len(namirnice_clean) > 300:
        st.warning("Unos je predug (max 300 znakova)." if st.session_state.jezik == "HR" else "Input is too long (max 300 characters).")
    else:
        with st.spinner(t["spinner"]):
            recept = st.write_stream(generiraj_recept(namirnice_clean, vrsta_obroka, st.session_state.jezik))
            st.session_state.trenutni_recept = recept
    
# Ocjenjivanje i zvjezdice            
if "zadnji_recepti" not in st.session_state:
    st.session_state.zadnji_recepti=[]            
if "trenutni_recept" not in st.session_state:
    st.session_state.trenutni_recept=None
if  st.session_state.trenutni_recept:
    st.markdown("---")
    st.success(t["success"])
    st.markdown("Ocijenite recept: ")
    ocjena=st.feedback("stars",key="recipe_rating")
    if ocjena is not None:
        st.write(f"Ocjena: {ocjena+1}/5 ⭐")
        try:
            sheet=spoji_sheets()
            from datetime import datetime
            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                st.session_state.namirnice_clean,
                vrsta_obroka,
                ocjena + 1,
                st.session_state.jezik
                
                
            ])
            st.success("Ocjena spremljena! ✅")
        except Exception as e:
            st.warning(f"Greška pri spremanju ocjene: {e}")
    
    st.download_button(
        label=t["download_button"],
        data=st.session_state.trenutni_recept,
        file_name="AI_Kuhar_Recept.txt",
        mime="text/plain"
    )

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
