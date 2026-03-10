import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load local .env file (for your local PC)
load_dotenv()

# Match the name "Groq" from your .env file
# This checks Streamlit Secrets first, then your local environment
api_key = st.secrets.get("Groq") or os.getenv("Groq")

if not api_key:
    st.error("API Key not found. Please add 'Groq' to your Streamlit Cloud Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# Page config
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="centered"
)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    model = st.selectbox(
        "Choose Model",
        ["llama-3.1-8b-instant"]
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.chat = []
        st.rerun()

    st.markdown("---")
    st.write("Simple LLM Chat App")
    st.write("Powered by Groq + Streamlit")

# Title
st.title("🤖 AI Chat Assistant")
st.markdown("Ask anything and get AI responses instantly.")

# Initialize session state for chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat history
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):

    # 1. Add user message to history
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Use streaming for a better UI experience
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat],
                stream=True
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)

            # 3. Save assistant reply to history
            st.session_state.chat.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")