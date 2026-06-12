import streamlit as st
import requests
import json
import os
from pypdf import PdfReader

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    st.session_state.messages = json.loads(content)
        except:
            st.session_state.messages = []


def save_chat_history(messages):
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)


feature = st.selectbox(
    "Select Feature",
    [
        "Chatbot",
        "Text Summarizer",
        "Simplify Answer",
        "PDF Reader"
    ]
)


def generate_ai_response(prompt):
    # Use the chat API for consistent response format
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "tinyllama",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    )

    data = response.json()
    return data.get("message", {}).get("content", "")


def summarize_text(text):

    prompt = f"""
Summarize the following text into concise bullet points:

{text}
"""

    return generate_ai_response(prompt)


def simplify_text(text):

    prompt = f"""
Explain the following in simple beginner-friendly language:

{text}
"""

    return generate_ai_response(prompt)
# -------------------------------------
# TEXT SUMMARIZER
# -------------------------------------

if feature == "Text Summarizer":

    st.header("📄 Text Summarizer")

    text = st.text_area(
        "Paste your text",
        height=250
    )

    if st.button("Summarize"):

        with st.spinner("Generating summary..."):

            result = summarize_text(text)

        st.success("Summary Generated")

        st.write(result)

# -------------------------------------
# SIMPLIFIED ANSWERS
# -------------------------------------

elif feature == "Simplify Answer":

    st.header("🧠 Simplify Text")

    text = st.text_area(
        "Paste difficult text",
        height=250
    )

    if st.button("Simplify"):

        with st.spinner("Simplifying..."):

            result = simplify_text(text)

        st.success("Done")

        st.write(result)

# -------------------------------------
# PDF READER
# -------------------------------------

elif feature == "PDF Reader":

    st.header("📚 PDF Reader")

    pdf_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if pdf_file:

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        st.text_area(
            "Extracted Text",
            text,
            height=400
        )
# -------------------------------------
# CHATBOT
# -------------------------------------

elif feature == "Chatbot":

    prompt = st.chat_input("Ask me anything...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        save_chat_history(st.session_state.messages)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "tinyllama",
                    "messages": st.session_state.messages,
                    "stream": False
                }
            )

            reply = response.json()["message"]["content"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        save_chat_history(st.session_state.messages)

        with st.chat_message("assistant"):
            st.markdown(reply)