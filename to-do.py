import streamlit as st
from groq import Groq
import os

# --- POSTAVKE ---

my_api_key = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="Varaždinski brzi kuhar", page_icon="🍳")

# --- SUČELJE ---
st.title("🍳 AI kuhar ")
st.caption("Powered by Groq (Llama 3.3)")
st.caption("Made by Filip (20% Digital)")
st.caption("Version: Beta")


col1,col2=st.columns([2,1])

with col1:
    namirnice_input=st.text_input("Što imate u frižideru danas?", placeholder="npr. jaja, piletina, kobasice...")

with col2:
    vrsta_obroka=st.selectbox(
        "Koja vrsta obroka?",
        ("Svejedno","Doručak","Ručak","Večera","Desert")
    )
    st.markdown("---")

gumb = st.button("Generiraj recept 🚀", type="primary")

# --- LOGIKA ---
def generiraj_recept(namirnice,obrok):
    if not my_api_key:
        return "⚠️ nema API ključa !"
    
    try:
        client = Groq(api_key=my_api_key)
        
        # Prompt je sada prilagođen za listu
        prompt = f"""
        Ti si vrhunski chef. Korisnik ima namirnice:{namirnice}
        Korisnik želi pripremiti:{obrok}.
        Napravi točno JEDAN recept na hrvatskom jeziku.
        Samo naslov, sastojci i priprema.
        """
        chat_completetion=client.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content":prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1

        )
        return chat_completetion.choices[0].message.content



    except Exception as e:
        return f"Greška: {str(e)}"

# --- PRIKAZ ---
if gumb:
    if namirnice_input:
        with st.spinner('Kombiniram sastojke...'):
            recept = generiraj_recept(namirnice_input, vrsta_obroka)
            st.markdown("---")
            st.success("Evo ideje!")
            st.markdown(recept)
    else:
        st.warning(" Frižider ti je prazan? Upiši nešto!")



st.markdown("-----")
paypal_url="https://paypal.me/filipvz"
col_lijevo,col_sredina,col_desno=st.columns([1,2,1])

with col_sredina:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("Sviđa ti se kuhar? Podrži ga!!!")
    
    st.link_button("☕ Kupi mi kavu (Doniraj)", url=paypal_url)


