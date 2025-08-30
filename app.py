import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_MESSAGES = 10
AI_PERSONALITY = "You are a friendly and helpful AI assistant, providing concise and accurate answers."


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": AI_PERSONALITY}]

st.set_page_config(page_title="🤖 Interactive AI Chatbot", page_icon="🤖")
st.title("🤖 Interactive AI Chatbot")

# User input
user_input = st.text_input("You:", key="input")

# Send button
if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    try:
        with st.spinner("AI is thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"⚠️ API Error: {e}")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='
                background-color:#A8DADC;  /* soft teal */
                color:#1D3557;             /* dark text */
                padding:10px;
                border-radius:8px;
                margin:5px 0;
                font-size:16px;
            '>
            <strong>You:</strong> {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
    elif msg["role"] == "assistant":
        st.markdown(
            f"""
            <div style='
                background-color:#F1FAEE;  /* very light green */
                color:#1D3557;             /* dark text */
                padding:10px;
                border-radius:8px;
                margin:5px 0;
                font-size:16px;
            '>
            <strong>Bot:</strong> {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

# Download chat history button
if st.button("Download Chat History"):
    chat_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("Download Chat", chat_text, file_name="chat_history.txt")
