import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load local .env file (for local development only)
load_dotenv()

# FIX: Check Streamlit Secrets first, then environment variables
# Note: Ensure you save it as "GROQ_API_KEY" in the Streamlit Cloud dashboard
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API Key not found. Please add 'GROQ_API_KEY' to your Streamlit Secrets or .env file.")
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
        ["llama-3.1-8b-instant", "llama3-70b-8192"]
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

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat history
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Use streaming for a better UI experience
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

    # Save assistant reply
    st.session_state.chat.append({"role": "assistant", "content": full_response})