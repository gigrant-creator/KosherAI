import streamlit as st
from huggingface_hub import InferenceClient

# --- CONFIGURATION ---
st.set_page_config(page_title="Kosher AI", page_icon="🥯")

# --- APP HEADER ---
st.title("🕎 The Bracha Bot")
st.subheader("Powered by Mistral (Raw Mode)")
st.caption("Status: SYSTEM ONLINE")

# --- SIDEBAR: API KEY INPUT ---
if "HF_TOKEN" in st.secrets:
    api_key = st.secrets["HF_TOKEN"]
else:
    api_key = st.sidebar.text_input("Paste Hugging Face Token:", type="password")

# --- MAIN APP LOGIC ---
if api_key:
    client = InferenceClient(api_key=api_key)

    food_input = st.text_input("What food are you eating?", placeholder="e.g., A slice of pizza")

    if st.button("Check Bracha"):
        if not food_input:
            st.warning("Please enter a food first!")
        else:
            with st.spinner("Consulting the digital Rabbi..."):
                try:
                    # MANUAL PROMPT ENGINEERING
                    # We manually format the text so the model knows it's a conversation.
                    # This bypasses the "chat_completion" errors.
                    prompt = f"""
                    [INST] You are an expert in Jewish Law (Halacha). 
                    The user is eating: {food_input}.
                    
                    1. Identify the food.
                    2. State the correct 'Bracha Rishona' (Blessing) in Hebrew and English.
                    3. Explain briefly why.
                    [/INST]
                    """
                    
                    # We use the raw 'text_generation' method. It works on almost ALL models.
                    response = client.text_generation(
                        model="mistralai/Mistral-7B-Instruct-v0.3", 
                        prompt=prompt, 
                        max_new_tokens=500,
                        temperature=0.7
                    )
                    
                    st.success("Analysis Complete!")
                    st.write(response)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("👈 System needs a Token. Check your Secrets or Sidebar.")
