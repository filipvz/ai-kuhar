import streamlit as st
from groq import Groq
import os

# --- POSTAVKE ---

my_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Varaždinski brzi kuhar", page_icon="🍳")

# --- SUČELJE ---
st.title("🍳 AI kuhar ")
st.caption("Powered by Groq (Llama 3.3)")
st.caption("Made by Filip (20% Digital)")


st.markdown("### Što sve imaš danas?")
namirnice_input = st.text_area(
    "Upiši sve namirnice odvojene zarezom:", 
    placeholder="npr. Jaja, luk, špek, pola paprike, vrhnje, stari kruh...",
    height=100
)

col1, col2 = st.columns([1, 2]) # Gumb će biti u užem stupcu
with col1:
    gumb = st.button("Generiraj recept 🚀", type="primary")

# --- LOGIKA ---
def generiraj_recept(popis_namirnica):
    if not in my_api_key:
        return "⚠️ Vrati svoj API ključ u kod!"
    
    try:
        client = Groq(api_key=my_api_key)
        
        # Prompt je sada prilagođen za listu
        prompt = f"""
        Ti si vrhunski chef. Korisnik ima ove namirnice na raspolaganju:
        {popis_namirnica}
        
        Zadatak:
        1. Smisli JEDAN najbolji mogući recept koristeći ŠTO VIŠE (ali ne nužno sve) navedene namirnice.
        2. Ako neka namirnica baš ne paše, ignoriraj ju.
        3. Recept mora biti na hrvatskom jeziku.
        4. Format: Naslov, Sastojci, Priprema (korak po korak). Bez filozofiranja.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile", 
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Greška: {str(e)}"

# --- PRIKAZ ---
if gumb:
    if namirnice_input:
        with st.spinner('Kombiniram sastojke...'):
            recept = generiraj_recept(namirnice_input)
            st.markdown("---")
            st.success("Evo ideje!")
            st.markdown(recept)
    else:

        st.warning(" Frižider ti je prazan? Upiši nešto!")


