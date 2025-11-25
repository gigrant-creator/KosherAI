import streamlit as st
from huggingface_hub import InferenceClient

# --- CONFIGURATION ---
st.set_page_config(page_title="Kosher AI", page_icon="🕎")

# --- APP HEADER ---
st.title("🕎 The Bracha Bot")
st.subheader("Powered by Hugging Face (Open Source AI)")

# --- SIDEBAR: API KEY INPUT ---
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Paste Hugging Face Token:", type="password")
st.sidebar.info("Get your free token at huggingface.co/settings/tokens")

# --- MAIN APP LOGIC ---
if api_key:
    # Initialize the AI Connection
    # We are using 'HuggingFaceH4/zephyr-7b-beta' - a very fast, smart free model
    client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=api_key)

    food_input = st.text_input("What food are you eating?", placeholder="e.g., A slice of pizza")

    if st.button("Check Bracha"):
        if not food_input:
            st.warning("Please enter a food first!")
        else:
            with st.spinner("Consulting the digital Rabbi..."):
                try:
                    # The Prompt to the AI
                    prompt_text = f"""
                    You are an expert in Jewish Law (Halacha). 
                    The user is eating: {food_input}.
                    
                    1. Identify the food.
                    2. State the correct 'Bracha Rishona' (Blessing) in Hebrew and English.
                    3. Explain briefly why (e.g., ingredients).
                    
                    Keep it short and friendly.
                    """
                    
                    # Send to AI
                    response = client.text_generation(
                        prompt_text, 
                        max_new_tokens=200, 
                        temperature=0.7
                    )
                    
                    # Display Result
                    st.success("Analysis Complete!")
                    st.write(response)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.error("Make sure your Token is correct and has 'Read' permissions!")
else:
    st.warning("👈 Please paste your Hugging Face Token in the sidebar to start.")
