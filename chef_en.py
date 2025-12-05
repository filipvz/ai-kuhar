import streamlit as st
from groq import Groq
import os

# --- POSTAVKE ---

my_api_key = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="Varaždinski brzi kuhar", page_icon="🍳")

# --- SUČELJE ---
st.title("🍳The AI Chef ")
st.caption("Powered by Groq (Llama 3.3)")
st.caption("Made by Filip (20% Digital)")
st.caption("Version: Beta")


col1,col2=st.columns([2,1])

with col1:
    fridge_input=st.text_input("What's in your fridge?", placeholder="e.g. eggs, bacon, onion...")

with col2:
    meal_choice=st.selectbox(
        "Which meal?",
        ("Any","Breakfest","Lunch","Dinner","Dessert")
    )
    st.markdown("---")

gumb = st.button("Generate Recipe 🚀", type="primary",use_container_width=True)

# --- LOGIKA ---
def generate_recipe_en(ingredients,meal_type):
    if not my_api_key:
        return "⚠️ nMissing API key !"
    
    try:
        client = Groq(api_key=my_api_key)
        
        # Prompt 
        prompt = f"""
        You are an experienced chef. 
        The user has these ingredients: {ingredients}.
        They want to make: {meal_type}.
        
        Task:
        Create exactly ONE recipe in English.
        Do not invent weird words. Use standard cooking terminology.
        Structure: Title, Ingredients, Instructions.
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
        return f"Error: {str(e)}"

# --- PRIKAZ ---
if gumb:
    if fridge_input:
        with st.spinner('Cooking up some magic...'):
            recept = generate_recipe_en(fridge_input,meal_choice)
            st.markdown("---")
            st.success("Enyoi your meal")
            st.markdown(recept)
    else:
        st.warning(" Your fridge is empty? type something!")



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
    st.write("Like the recipe? Support the Chef:")
    
    st.link_button("☕ Buy me a coffe (Donate)", url=paypal_url)

