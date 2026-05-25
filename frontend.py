from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import requests
import uuid

BACKEND_URL = "https://mayi-disha-backend-production.up.railway.app"

st.set_page_config(
    page_title="Nayi Disha",
    page_icon="🌸",
    layout="wide"
)

# ==========================
# GLOBAL CSS
# ==========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Nunito:wght@300;400;600;700&display=swap');

/* ── ROOT THEME ── */
:root {
    --rose:    #f9a8d4;
    --blush:   #fce7f3;
    --lavender:#e9d5ff;
    --lilac:   #c4b5fd;
    --mint:    #a7f3d0;
    --sky:     #bae6fd;
    --cream:   #fef3c7;
    --dark-bg: #0f0e17;
    --card-bg: #1a1828;
    --card2:   #201e30;
    --border:  rgba(249,168,212,0.18);
    --text:    #f0e6ff;
    --muted:   #9ca3af;
    --glow:    rgba(196,181,253,0.12);
}

/* ── APP BACKGROUND ── */
.stApp {
    background: var(--dark-bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(196,181,253,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(249,168,212,0.07) 0%, transparent 60%);
    font-family: 'Nunito', sans-serif;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #1e1b30 0%, #1a1828 50%, #1e1b2e 100%);
    border: 1px solid var(--border);
    border-radius: 28px;
    padding: 48px 40px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 28px;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%; transform: translateX(-50%);
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(196,181,253,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Quicksand', sans-serif;
    font-size: 3.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f9a8d4 0%, #c4b5fd 50%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 10px;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 1.1rem;
    color: #a78bfa;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.3px;
}
.hero-dots {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin-top: 20px;
}
.hero-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--lilac);
    opacity: 0.4;
}
.hero-dot.active { opacity: 1; background: var(--rose); }

/* ── STAT CARDS ── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 26px;
}
.stat-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px 18px;
    text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
    cursor: default;
}
.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(196,181,253,0.4);
    background: #1f1d31;
}
.stat-icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 10px;
    filter: drop-shadow(0 0 8px rgba(196,181,253,0.5));
}
.stat-label {
    font-family: 'Quicksand', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 4px;
}
.stat-desc {
    font-size: 0.78rem;
    color: var(--muted);
    margin: 0;
}

/* ── DIVIDER ── */
.pretty-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0 20px;
}
.pretty-divider span {
    height: 1px;
    flex: 1;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
}
.pretty-divider p {
    font-size: 0.8rem;
    color: #6b7280;
    margin: 0;
    white-space: nowrap;
    font-family: 'Quicksand', sans-serif;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessageContent"] {
    font-family: 'Nunito', sans-serif;
    font-size: 0.97rem;
    line-height: 1.65;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, #2d1f3d, #261d38) !important;
    border: 1px solid rgba(196,181,253,0.2) !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 14px 18px !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: linear-gradient(135deg, #1c2235, #182038) !important;
    border: 1px solid rgba(186,230,253,0.15) !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 14px 18px !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] textarea {
    background: #1a1828 !important;
    border: 1px solid rgba(196,181,253,0.25) !important;
    border-radius: 16px !important;
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(196,181,253,0.6) !important;
    box-shadow: 0 0 0 3px rgba(196,181,253,0.08) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #6b7280 !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0d0c18 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stToggle label,
[data-testid="stSidebar"] p {
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
}
[data-testid="stSidebar"] select {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}

/* Sidebar title */
.sidebar-title {
    font-family: 'Quicksand', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f9a8d4, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
}

/* Sidebar badge */
.sidebar-badge {
    display: inline-block;
    background: rgba(196,181,253,0.12);
    border: 1px solid rgba(196,181,253,0.25);
    border-radius: 100px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #c4b5fd;
    font-family: 'Quicksand', sans-serif;
    font-weight: 600;
    margin-bottom: 18px;
}

/* Sidebar tip */
.sidebar-tip {
    background: rgba(167,243,208,0.07);
    border: 1px solid rgba(167,243,208,0.15);
    border-radius: 14px;
    padding: 14px;
    margin-top: 20px;
}
.sidebar-tip p {
    font-size: 0.82rem !important;
    color: #6ee7b7 !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}

/* ── BUTTON ── */
.stButton > button {
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 14px !important;
    background: rgba(196,181,253,0.08) !important;
    border: 1px solid rgba(196,181,253,0.28) !important;
    color: #c4b5fd !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: rgba(249,168,212,0.12) !important;
    border-color: rgba(249,168,212,0.4) !important;
    color: var(--rose) !important;
    transform: translateY(-2px) !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] > div {
    border-color: #c4b5fd transparent transparent transparent !important;
}

/* ── SELECTBOX & TOGGLE ── */
[data-baseweb="select"] > div {
    background: var(--card-bg) !important;
    border-color: var(--border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
}

/* ── WELCOME CARD ── */
.welcome-card {
    background: linear-gradient(135deg, rgba(196,181,253,0.06), rgba(249,168,212,0.04));
    border: 1px dashed rgba(196,181,253,0.2);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    margin-bottom: 16px;
}
.welcome-card p {
    color: var(--muted);
    font-size: 0.92rem;
    margin: 0;
    line-height: 1.6;
}
.welcome-card .big-emoji {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 12px;
    filter: drop-shadow(0 0 12px rgba(249,168,212,0.4));
}

/* ── MOOD CHIPS ── */
.mood-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 14px;
}
.mood-chip {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.82rem;
    color: #d8b4fe;
    font-family: 'Quicksand', sans-serif;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}
.mood-chip:hover {
    background: rgba(196,181,253,0.12);
    border-color: rgba(196,181,253,0.45);
    transform: translateY(-2px);
}

/* ── PULSE ANIMATION ── */
@keyframes pulse-soft {
    0%, 100% { opacity: 0.6; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}
.pulse { animation: pulse-soft 3s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)


# ==========================
# SESSION STATE
# ==========================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌸 Nayi Disha</div>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-badge">✦ AI Companion</span>', unsafe_allow_html=True)

    st.markdown("**Support Type**")
    support = st.selectbox(
        "Support Type",
        ["child", "women"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    allow_search = st.toggle("🔍 Enable Web Search", value=False)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("""
    <div class="sidebar-tip">
        <p>💡 This is a safe, private space. Share what you feel comfortable with — there's no pressure.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:0.75rem; color:#4b5563; text-align:center; font-family:'Quicksand',sans-serif;">
        Made with 💜 for healing & growth
    </p>
    """, unsafe_allow_html=True)


# ==========================
# HERO
# ==========================
st.markdown("""
<div class="hero">
    <h1 class="hero-title">🌸 Nayi Disha</h1>
    <p class="hero-sub">Your gentle AI companion — here to listen, support & heal</p>
    <div class="hero-dots">
        <div class="hero-dot active"></div>
        <div class="hero-dot"></div>
        <div class="hero-dot"></div>
        <div class="hero-dot"></div>
        <div class="hero-dot"></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================
# STAT CARDS
# ==========================
st.markdown("""
<div class="stat-row">
    <div class="stat-card">
        <span class="stat-icon pulse">🤝</span>
        <p class="stat-label">Emotional Support</p>
        <p class="stat-desc">Always here for you</p>
    </div>
    <div class="stat-card">
        <span class="stat-icon pulse">🧠</span>
        <p class="stat-label">AI Companion</p>
        <p class="stat-desc">Thoughtful & empathetic</p>
    </div>
    <div class="stat-card">
        <span class="stat-icon pulse">🔒</span>
        <p class="stat-label">Safe Space</p>
        <p class="stat-desc">Private & judgement-free</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================
# DIVIDER
# ==========================
st.markdown("""
<div class="pretty-divider">
    <span></span>
    <p>✦ your conversation ✦</p>
    <span></span>
</div>
""", unsafe_allow_html=True)


# ==========================
# WELCOME / EMPTY STATE
# ==========================
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <span class="big-emoji">🌷</span>
        <p>Welcome, you're in a safe and caring space.<br>
        Feel free to share what's on your heart — Nayi Disha is here to listen without judgement.</p>
        <div class="mood-chips">
            <span class="mood-chip">😔 Feeling sad</span>
            <span class="mood-chip">😰 Feeling anxious</span>
            <span class="mood-chip">💬 Need to talk</span>
            <span class="mood-chip">🌱 Want to grow</span>
            <span class="mood-chip">😶 Don't know yet</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================
# CHAT MESSAGES
# ==========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ==========================
# CHAT INPUT
# ==========================
prompt = st.chat_input("Share what's on your mind... 🌸")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    payload = {
        "user_id": 1,
        "session_id": st.session_state.session_id,
        "model_name": "llama-3.3-70b-versatile",
        "support_type": support,
        "messages": [prompt],
        "allow_search": allow_search
    }

    with st.spinner("🌸 Nayi Disha is listening..."):
        try:
            r = requests.post(f"{BACKEND_URL}/chat", json=payload)
            response = r.json()["response"]
        except Exception as e:
            response = "I'm having trouble connecting right now. Please try again in a moment. 💜"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()