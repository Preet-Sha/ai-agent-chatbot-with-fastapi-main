import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Nayi Disha",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Nayi Disha")
st.write("Your AI Assistant")

# Model Mapping
model_options = {
    "Nayi Disha": "llama-3.3-70b-versatile"
}

selected_option = st.selectbox(
    "Select Assistant",
    options=list(model_options.keys()),
    index=0
)

# Actual model used internally
model = model_options[selected_option]

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
prompt = st.chat_input("Ask Nayi Disha...")

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Backend call
    try:
        payload = {
            "message": prompt,
            "model_name": model
        }

        response = requests.post(
            "http://127.0.0.1:9999/chat",
            json=payload
        )

        if response.status_code == 200:

            ai_response = response.json()["response"]

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

            with st.chat_message("assistant"):
                st.markdown(ai_response)

        else:
            st.error("Backend Error")

    except Exception as e:
        st.error(f"Error: {e}")