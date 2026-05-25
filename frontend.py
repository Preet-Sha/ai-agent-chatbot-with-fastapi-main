from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from database import *

from ai_agent import *


st.set_page_config(
    page_title="Safe Support Chatbot",
    layout="centered"
)


st.title(
    "🌸 Safe Support Chatbot"
)


# ==========================
# SESSION STATE
# ==========================
if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "user_id" not in st.session_state:

    st.session_state.user_id = None


if "support" not in st.session_state:

    st.session_state.support = None


if "name" not in st.session_state:

    st.session_state.name = None



# ==========================
# LOGIN / SIGNUP
# ==========================
if not st.session_state.logged_in:

    page = st.sidebar.radio(

        "Account",

        [

            "Login",

            "Signup"

        ]
    )


    # ======================
    # SIGNUP
    # ======================
    if page == "Signup":

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


        support = st.selectbox(

            "Support Type",

            [

                "child",

                "women"

            ]
        )


        if st.button(
            "Signup"
        ):

            ok = create_user(

                name,

                email,

                password,

                support
            )


            if ok:

                st.success(
                    "Account created"
                )

            else:

                st.error(
                    "Email already exists"
                )


    # ======================
    # LOGIN
    # ======================
    if page == "Login":

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

            user = login_user(

                email,

                password
            )


            if user:

                st.session_state.logged_in = True

                st.session_state.user_id = user[0]

                st.session_state.name = user[1]

                st.session_state.support = user[2]

                st.rerun()


            else:

                st.error(
                    "Invalid credentials"
                )



# ==========================
# CHAT SECTION
# ==========================
else:

    st.sidebar.success(

        f"Logged in as {st.session_state.name}"
    )


    if st.sidebar.button(
        "Logout"
    ):

        st.session_state.clear()

        st.rerun()



    model = st.selectbox(

        "Model",

        [

            "llama-3.3-70b-versatile",

            

        ]
    )


    allow_search = st.checkbox(
        "Allow Web Search"
    )


    history = get_history(

        st.session_state.user_id
    )


    for msg in history:

        st.write(
            msg
        )


    prompt = st.chat_input(
        "Type your message"
    )


    if prompt:

        save_message(

            st.session_state.user_id,

            "user",

            prompt
        )


        history = get_history(

            st.session_state.user_id
        )


        reply = get_response_from_ai_agent(

            model,

            history,

            allow_search,

            st.session_state.support
        )


        save_message(

            st.session_state.user_id,

            "assistant",

            reply
        )


        st.rerun()