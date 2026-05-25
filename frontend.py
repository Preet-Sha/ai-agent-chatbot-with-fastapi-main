from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
import uuid


API_URL = "http://127.0.0.1:9999"


# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Safe Support Chatbot",
    layout="centered"
)

st.title("🌸 Safe Support Chatbot")


# ==========================
# SESSION VARIABLES
# ==========================
if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


if "session_id" not in st.session_state:

    st.session_state.session_id = str(
        uuid.uuid4()
    )


# ==========================
# LOGIN / SIGNUP
# ==========================
if not st.session_state.logged_in:

    menu = st.sidebar.radio(

        "Account",

        [

            "Login",

            "Signup"

        ]
    )


    # ==========================
    # SIGNUP
    # ==========================
    if menu == "Signup":

        st.subheader(
            "Create Account"
        )

        name = st.text_input(
            "Name"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        support_type = st.selectbox(

            "Support Type",

            [

                "child",

                "women"

            ]
        )


        if st.button(
            "Signup"
        ):

            response = requests.post(

                f"{API_URL}/signup",

                json={

                    "name":
                    name,

                    "email":
                    email,

                    "password":
                    password,

                    "support_type":
                    support_type
                }
            )


            if response.status_code == 200:

                data = response.json()

                if data["success"]:

                    st.success(
                        "Account Created"
                    )

                else:

                    st.error(
                        "Email already exists"
                    )

            else:

                st.error(
                    response.text
                )


    # ==========================
    # LOGIN
    # ==========================
    if menu == "Login":

        st.subheader(
            "Login"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "Login"
        ):

            response = requests.post(

                f"{API_URL}/login",

                json={

                    "email":
                    email,

                    "password":
                    password
                }
            )


            if response.status_code == 200:

                data = response.json()


                if data["success"]:

                    st.session_state.logged_in = True

                    st.session_state.user_id = data[
                        "user_id"
                    ]

                    st.session_state.user_name = data[
                        "name"
                    ]

                    st.session_state.support = data[
                        "support_type"
                    ]

                    st.success(
                        "Login Successful"
                    )

                    st.rerun()

                else:

                    st.error(
                        data["message"]
                    )

            else:

                st.error(
                    response.text
                )



# ==========================
# CHAT SCREEN
# ==========================
else:

    st.sidebar.success(

        f"Logged in as: {st.session_state.user_name}"

    )


    if st.sidebar.button(
        "Logout"
    ):

        st.session_state.logged_in = False

        st.session_state.chat_history = []

        st.rerun()


    st.write(

        f"Support Mode: **{st.session_state.support}**"

    )


    provider = st.selectbox(

        "Provider",

        [

            "Nayi Disha",


        ]
    )


    if provider == "Nayi Disha":

        model = "llama-3.3-70b-versatile"

    else:

        model = st.selectbox(

            "Model",

            [

                "llama-3.3-70b-versatile",

                "mixtral-8x7b-32768"

            ]
        )


    allow_search = st.checkbox(
        "Allow Web Search"
    )


    user_msg = st.chat_input(
        "Type here..."
    )


    if user_msg:

        st.session_state.chat_history.append(

            (

                "user",

                user_msg

            )

        )


        payload = {

            "user_id":

            st.session_state.user_id,

            "session_id":

            st.session_state.session_id,

            "model_name":

            model,

            "model_provider":

            provider,

            "support_type":

            st.session_state.support,

            "messages":

            [

                user_msg

            ],

            "allow_search":

            allow_search
        }


        response = requests.post(

            f"{API_URL}/chat",

            json=payload
        )


        if response.status_code == 200:

            data = response.json()

            ai_reply = data[
                "response"
            ]


            st.session_state.chat_history.append(

                (

                    "assistant",

                    ai_reply

                )

            )

        else:

            st.error(
                response.text
            )


    # SHOW CHAT
    for role, msg in st.session_state.chat_history:

        with st.chat_message(
            role
        ):

            st.write(
                msg
            )