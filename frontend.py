# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
import requests
import uuid


BACKEND_URL = "http://127.0.0.1:9999"


st.set_page_config(
    page_title="Mayi Disha",
    page_icon="🌸",
    layout="wide"
)


# ==========================
# CUSTOM CSS
# ==========================

st.markdown(
    """
    <style>

    .main{
        background: linear-gradient(
        135deg,
        #fff7f5,
        #fff0f6,
        #f8f5ff
        );
    }

    .hero{
        padding:25px;
        border-radius:20px;

        background:
        linear-gradient(
        135deg,
        #ffdde1,
        #ee9ca7
        );

        color:black;

        text-align:center;

        margin-bottom:20px;

        box-shadow:
        0px 10px 30px
        rgba(0,0,0,0.08);
    }

    .hero h1{
        font-size:42px;
    }

    .hero p{
        font-size:18px;
    }

    .card{

        background:white;

        padding:18px;

        border-radius:18px;

        box-shadow:
        0 6px 20px
        rgba(0,0,0,0.05);

        margin-bottom:15px;
    }

    .stChatMessage{

        border-radius:18px;

        padding:8px;

        background:white;

        margin-bottom:8px;
    }

    </style>
    """,

    unsafe_allow_html=True
)


# ==========================
# HEADER
# ==========================

st.markdown(
    """
    <div class="hero">

    <h1>🌸 Mayi Disha</h1>

    <p>

    AI Companion for Emotional Support

    </p>

    </div>

    """,

    unsafe_allow_html=True
)


# ==========================
# SESSION
# ==========================

if "session_id" not in st.session_state:

    st.session_state.session_id = str(
        uuid.uuid4()
    )


if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.markdown(
        "## 🌷 Support Settings"
    )

    support = st.selectbox(

        "Support Type",

        [

            "child",

            "women"

        ]
    )


    allow_search = st.toggle(
        "Enable Search"
    )


    st.markdown("---")


    if support=="child":

        st.info(
            "Gentle support mode enabled"
        )

    else:

        st.info(
            "Women support mode enabled"
        )


    if st.button(
        "🗑 Clear Chat"
    ):

        st.session_state.messages=[]

        st.session_state.session_id = str(
            uuid.uuid4()
        )

        st.rerun()


# ==========================
# FEATURE CARDS
# ==========================

c1,c2,c3 = st.columns(3)

with c1:

    st.markdown(

        """
        <div class="card">

        🤝 Emotional Support

        </div>

        """,

        unsafe_allow_html=True
    )

with c2:

    st.markdown(

        """
        <div class="card">

        🧠 AI Companion

        </div>

        """,

        unsafe_allow_html=True
    )

with c3:

    st.markdown(

        """
        <div class="card">

        🔒 Safe Space

        </div>

        """,

        unsafe_allow_html=True
    )


st.markdown("---")


# ==========================
# CHAT HISTORY
# ==========================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )


prompt = st.chat_input(
    "Share your thoughts..."
)


# ==========================
# CHAT
# ==========================

if prompt:

    st.session_state.messages.append(

        {

            "role":"user",

            "content":prompt

        }

    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )


    payload = {

        "user_id":1,

        "session_id":
        st.session_state.session_id,

        "model_name":
        "llama-3.3-70b-versatile",

        "support_type":
        support,

        "messages":
        [prompt],

        "allow_search":
        allow_search

    }


    with st.spinner(
        "Mayi Disha is thinking..."
    ):

        r = requests.post(

            f"{BACKEND_URL}/chat",

            json=payload

        )


        response = r.json()[
            "response"
        ]


    st.session_state.messages.append(

        {

            "role":"assistant",

            "content":response

        }

    )


    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            response
        )


    st.rerun()