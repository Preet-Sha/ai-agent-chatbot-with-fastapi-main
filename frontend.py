from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
import uuid

BACKEND_URL = "https://mayi-disha-backend-production.up.railway.app"

st.set_page_config(
    page_title="Mayi Disha",
    page_icon="🌸",
    layout="wide"
)

# ==========================
# CSS
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
#1e293b
);
}

/* HERO */

.hero{

padding:40px;

border-radius:25px;

background:
linear-gradient(
135deg,
#fbcfe8,
#f9a8d4
);

text-align:center;

box-shadow:
0px 10px 30px rgba(
0,
0,
0,
0.25
);

margin-bottom:20px;

transition:.3s;

}

.hero:hover{

transform:
translateY(-4px);

}


.hero h1{

font-size:60px;

font-weight:800;

color:black;

}

.hero p{

font-size:22px;

color:#1f2937;

}


/* CARDS */

.card{

background:
rgba(
255,
255,
255,
0.08
);

padding:25px;

border-radius:20px;

text-align:center;

font-size:20px;

font-weight:600;

color:white;

border:
1px solid rgba(
255,
255,
255,
0.1
);

transition:.3s;

margin-bottom:10px;

}

.card:hover{

transform:
translateY(-8px);

background:
rgba(
236,
72,
153,
0.2
);

}


/* SIDEBAR */

[data-testid="stSidebar"]{

background:
#111827;

}


/* BUTTON */

.stButton>button{

border-radius:14px;

background:
linear-gradient(
135deg,
#ec4899,
#f472b6
);

color:white;

font-weight:700;

border:none;

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

    st.title(
        "🌷 Settings"
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


    if st.button(
        "🗑 Clear Chat"
    ):

        st.session_state.messages=[]

        st.session_state.session_id = str(
            uuid.uuid4()
        )

        st.rerun()


# ==========================
# CARDS
# ==========================

c1,c2,c3=st.columns(3)

with c1:

    st.markdown(
    """
    <div class="card">
    🤝 <br>
    Emotional Support
    </div>
    """,
    unsafe_allow_html=True
    )


with c2:

    st.markdown(
    """
    <div class="card">
    🧠 <br>
    AI Companion
    </div>
    """,
    unsafe_allow_html=True
    )


with c3:

    st.markdown(
    """
    <div class="card">
    🔒 <br>
    Safe Space
    </div>
    """,
    unsafe_allow_html=True
    )


st.divider()


# ==========================
# CHAT
# ==========================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )


prompt = st.chat_input(
    "Share your thoughts..."
)


if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
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

    st.rerun()