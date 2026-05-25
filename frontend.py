# Uncomment if not using pipenv
# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
import requests

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Safe Support Chatbot",
    layout="centered"
)

st.title("🌸 Safe Support Chatbot")

st.write(
    """
    A safe emotional support assistant for children and women.
    """
)


# ==========================
# SUPPORT TYPE
# ==========================
support_type = st.radio(

    "Choose Support Type",

    [

        "child",

        "women"

    ],

    horizontal=True
)


# ==========================
# MODEL SELECTION
# ==========================
MODEL_NAMES_GROQ = [

    "llama-3.3-70b-versatile",

    "mixtral-8x7b-32768"

]

MODEL_NAMES_OPENAI = [

    "gpt-4o-mini"

]


provider = st.radio(

    "Select Provider",

    (

        "Groq",

        "OpenAI"

    )
)


if provider == "Groq":

    selected_model = st.selectbox(

        "Select Groq Model",

        MODEL_NAMES_GROQ
    )

else:

    selected_model = st.selectbox(

        "Select OpenAI Model",

        MODEL_NAMES_OPENAI
    )


# ==========================
# SEARCH
# ==========================
allow_web_search = st.checkbox(
    "Allow Web Search"
)


# ==========================
# USER INPUT
# ==========================
placeholder_text = (

    "Tell me what happened..."

    if support_type == "women"

    else

    "You can talk to me. What happened?"
)


user_query = st.text_area(

    "Message",

    height=180,

    placeholder=placeholder_text
)


API_URL = "http://127.0.0.1:9999/chat"


# ==========================
# SEND MESSAGE
# ==========================
if st.button("Send"):

    if user_query.strip() == "":

        st.warning(
            "Please enter a message"
        )

    else:

        payload = {

            "model_name":
            selected_model,

            "model_provider":
            provider,

            "support_type":
            support_type,

            "messages":
            [user_query],

            "allow_search":
            allow_web_search
        }


        try:

            response = requests.post(
                API_URL,
                json=payload
            )


            if response.status_code == 200:

                response_data = response.json()

                if response_data.get(
                    "status"
                ) == "error":

                    st.error(
                        response_data[
                            "message"
                        ]
                    )

                else:

                    st.subheader(
                        "Support Response"
                    )

                    st.write(

                        response_data[
                            "response"
                        ]

                    )

            else:

                st.error(
                    "Backend connection failed"
                )


        except Exception as e:

            st.error(
                str(e)
            )