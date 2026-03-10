import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


client = Groq(api_key=os.getenv("Groq"))


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


# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []


# Display chat history
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
prompt = st.chat_input("Type your message...")


if prompt:


    # Add user message
    st.session_state.chat.append({
        "role": "user",
        "content": prompt
    })


    with st.chat_message("user"):
        st.markdown(prompt)


    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):


            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.chat
            )


            reply = response.choices[0].message.content


            st.markdown(reply)


    # Save assistant reply
    st.session_state.chat.append({
        "role": "assistant",
        "content": reply
    })