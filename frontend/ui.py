import streamlit as st
import requests


# Backend URL (Flask server)
BACKEND_URL = "http://127.0.0.1:5000/chat"


# Page title
st.title("HR Policy Chatbot (RAG + Gemini)")
st.write("Ask questions only about HR policies.")


# Chat history memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# Show previous messages
for role, msg in st.session_state.messages:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)


# Input box
user_input = st.chat_input("Type your question...")


# When user sends message
if user_input:

    # show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append(("user", user_input))

    # send request to Flask backend
    response = requests.post(
        BACKEND_URL,
        json={"query": user_input}
    )

    if response.status_code == 200:
        data = response.json()
        answer = data["answer"]
    else:
        answer = "Server error"

    # show bot reply
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append(("assistant", answer))
