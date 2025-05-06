import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"  

st.set_page_config(page_title="Support Chatbot", page_icon="💬")
st.title("Support Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question:")

if query:
    with st.spinner("Thinking..."):
        res = requests.post(API_URL, json={"question": query})
        if res.status_code == 200:
            answer = res.json().get("answer", "Error.")
            sources = res.json().get("sources", [])
            st.session_state.history.append((query, answer, sources))
        else:
            st.error("Failed to get a response from the server.")

for q, a, s in reversed(st.session_state.history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")
