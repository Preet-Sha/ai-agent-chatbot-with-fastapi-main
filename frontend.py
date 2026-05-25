from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from database import *
from ai_agent import *


st.set_page_config(
    page_title="Safe Support Chatbot"
)

st.title(
    "🌸 Safe Support Chatbot"
)


if "logged_in" not in st.session_state:

    st.session_state.logged_in=False


if "user_id" not in st.session_state:

    st.session_state.user_id=None


if "support" not in st.session_state:

    st.session_state.support=None


if "name" not in st.session_state:

    st.session_state.name=None



if not st.session_state.logged_in:

    page = st.sidebar.radio(

        "Account",

        [

            "Login",

            "Signup"

        ]
    )


    if page=="Signup":

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
                    "Email exists"
                )



    if page=="Login":

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

                st.session_state.logged_in=True

                st.session_state.user_id=user[0]

                st.session_state.name=user[1]

                st.session_state.support=user[2]

                st.rerun()

            else:

                st.error(
                    "Invalid credentials"
                )



else:

    st.sidebar.success(

        st.session_state.name
    )


    if st.sidebar.button(
        "Logout"
    ):

        st.session_state.clear()

        st.rerun()


    allow_search = st.checkbox(
        "Allow Search"
    )


    history = get_history(

        st.session_state.user_id
    )


    for role,msg in history:

        with st.chat_message(
            role
        ):

            st.markdown(msg)


    prompt = st.chat_input(
        "Type..."
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


        messages = [

            x[1]

            for x in history

        ]


        reply = get_response_from_ai_agent(

            "llama-3.3-70b-versatile",

            messages,

            allow_search,

            st.session_state.support
        )


        save_message(

            st.session_state.user_id,

            "assistant",

            reply
        )


        st.rerun()