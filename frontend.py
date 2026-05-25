from dotenv import load_dotenv
load_dotenv()

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

.stApp{

background:
linear-gradient(
135deg,
#0f172a,
#111827,
#1e1b4b
);

color:white;

}


/* HERO */

.hero{

padding:45px;

border-radius:28px;

background:
linear-gradient(
135deg,
rgba(255,192,203,0.25),
rgba(236,72,153,0.18)
);

backdrop-filter: blur(18px);

border:
1px solid rgba(
255,
255,
255,
0.12
);

text-align:center;

box-shadow:
0px 12px 40px
rgba(
0,
0,
0,
0.35
);

transition:0.4s;

}

.hero:hover{

transform:
translateY(-5px);

box-shadow:
0px 18px 50px
rgba(
255,
105,
180,
0.25
);

}

.hero h1{

font-size:64px;

font-weight:800;

color:white;

}

.hero p{

font-size:22px;

color:#f3f4f6;

}


/* FEATURE CARDS */

.card{

background:
rgba(
255,
255,
255,
0.08
);

backdrop-filter:
blur(12px);

padding:28px;

border-radius:22px;

text-align:center;

font-size:22px;

font-weight:600;

color:white;

border:

1px solid rgba(
255,
255,
255,
0.12
);

transition:all .35s ease;

box-shadow:
0px 8px 25px
rgba(
0,
0,
0,
0.25
);

height:120px;

display:flex;

justify-content:center;

align-items:center;

}


.card:hover{

transform:

translateY(-10px)

scale(1.04);

background:

linear-gradient(
135deg,
rgba(
255,
192,
203,
0.30
),

rgba(
236,
72,
153,
0.25
)

);

box-shadow:

0px 15px 35px

rgba(
236,
72,
153,
0.30
);

cursor:pointer;

}


/* CHAT */

.stChatMessage{

background:

rgba(
255,
255,
255,
0.08
);

backdrop-filter:
blur(10px);

border-radius:20px;

padding:12px;

margin-bottom:10px;

border:

1px solid rgba(
255,
255,
255,
0.08
);

}


/* SIDEBAR */

[data-testid="stSidebar"]{

background:

linear-gradient(

180deg,

#111827,

#1e293b

);

}


/* BUTTON */

.stButton>button{

width:100%;

border-radius:16px;

background:

linear-gradient(

135deg,

#ec4899,

#f472b6

);

color:white;

border:none;

font-weight:700;

transition:.3s;

}


.stButton>button:hover{

transform:

translateY(-3px);

box-shadow:

0px 8px 20px

rgba(
236,
72,
153,
0.4
);

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

<h1>

🌸 Mayi Disha

</h1>

<p>

AI Companion for Emotional Support & Healing

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

    st.session_state.messages=[]


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
            "Gentle Support Mode"
        )

    else:

        st.info(
            "Women Support Mode"
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

c1,c2,c3=st.columns(3)

with c1:

    st.markdown(

    """

    <div class="card">

    🤝<br>

    Emotional Support

    </div>

    """,

    unsafe_allow_html=True

    )


with c2:

    st.markdown(

    """

    <div class="card">

    🧠<br>

    AI Companion

    </div>

    """,

    unsafe_allow_html=True

    )


with c3:

    st.markdown(

    """

    <div class="card">

    🔒<br>

    Safe Space

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
        "🌸 Mayi Disha is listening..."
    ):

        r=requests.post(

            f"{BACKEND_URL}/chat",

            json=payload

        )


        response=r.json()[
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