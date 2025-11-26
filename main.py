import streamlit as st
from huggingface_hub import InferenceClient

# --- CONFIGURATION ---
st.set_page_config(page_title="Kosher AI", page_icon="🥯")

# --- APP HEADER ---
st.title("🕎 The Bracha Bot")
st.subheader("Powered by Llama 3 (Conversational)")
st.caption("Status: SYSTEM ONLINE")

# --- SIDEBAR: API KEY INPUT ---
if "HF_TOKEN" in st.secrets:
    api_key = st.secrets["HF_TOKEN"]
else:
    api_key = st.sidebar.text_input("Paste Hugging Face Token:", type="password")

# --- MAIN APP LOGIC ---
if api_key:
    # Initialize the AI Connection
    client = InferenceClient(api_key=api_key)

    food_input = st.text_input("What food are you eating?", placeholder="e.g., A slice of pizza")

    if st.button("Check Bracha"):
        if not food_input:
            st.warning("Please enter a food first!")
        else:
            with st.spinner("Consulting the digital Rabbi..."):
                try:
                    # THE FIX: We use Llama 3. It is strictly a CHAT model.
                    # This aligns perfectly with the "Conversational" requirement of the server.
                    messages = [
                        {
                            "role": "user", 
                            "content": f"I am eating {food_input}. 1. Identify the food. 2. State the correct Bracha Rishona. 3. Briefly explain why."
                        }
                    ]
                    
                    response = client.chat_completion(
                        model="meta-llama/Meta-Llama-3-8B-Instruct", 
                        messages=messages, 
                        max_tokens=500
                    )
                    
                    answer = response.choices[0].message.content
                    
                    st.success("Analysis Complete!")
                    st.write(answer)
                    
                except Exception as e:
                    # If Llama fails, we show the raw error to debug
                    st.error(f"Error: {e}")
                    st.info("Tip: If the server is busy, wait 30 seconds and try again.")
else:
    st.warning("👈 System needs a Token. Check your Secrets or Sidebar.")
