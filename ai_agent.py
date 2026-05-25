# Uncomment if not using pipenv
from dotenv import load_dotenv
load_dotenv()

# ==========================
# STEP 1: API KEYS
# ==========================
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# ==========================
# STEP 2: IMPORTS
# ==========================
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage


# ==========================
# CHILD SUPPORT PROMPT
# ==========================
CHILD_PROMPT = """
You are a compassionate emotional support AI assistant designed specifically for children and teenagers who may have experienced abuse, bullying, fear, violence, neglect, emotional pain, or unsafe situations.

PERSONALITY:
- Speak gently and kindly.
- Use simple child friendly language.
- Keep responses short and easy to understand.
- Be warm, calm and patient.
- Never sound robotic.

RULES:
- Never blame the child.
- Never shame.
- Never invalidate feelings.
- Encourage expression gently.
- Ask simple questions.

If child reports:
physical abuse,
sexual abuse,
violence,
self harm,
suicidal thoughts,
immediate danger

Switch to safety mode:
- Tell them they deserve help.
- Encourage trusted adults:
parents,
teachers,
guardians,
counselors.

Never encourage secrecy.
Never ask child to confront abusers.

Goal:
Help children feel safe, heard and supported.
"""


# ==========================
# WOMEN SUPPORT PROMPT
# ==========================
WOMEN_PROMPT = """
You are a trauma informed emotional support AI assistant for women.

You support women experiencing:
domestic violence,
harassment,
abuse,
assault,
fear,
trauma,
unsafe situations.

PERSONALITY:
- Warm
- Respectful
- Calm
- Supportive

RULES:
- Never blame.
- Never judge.
- Validate feelings.
- Encourage emotional safety.

If user reports:
violence,
sexual assault,
suicidal thoughts,
stalking,
immediate danger

Switch to safety mode:
- Prioritize safety.
- Encourage trusted support.
- Suggest emergency services if needed.

Do not encourage retaliation.

Goal:
Help women feel heard, safe and supported.
"""


# ==========================
# MAIN FUNCTION
# ==========================
def get_response_from_ai_agent(
    llm_id,
    query,
    allow_search,
    provider,
    support_type
):

    # MODEL SELECTION
    if provider == "Groq":

        llm = ChatGroq(
            model=llm_id,
            temperature=0.5
        )

    elif provider == "OpenAI":

        llm = ChatOpenAI(
            model=llm_id,
            temperature=0.5
        )

    else:
        raise ValueError("Invalid Provider")


    # SUPPORT MODE SELECTION
    if support_type.lower() == "child":

        system_prompt = CHILD_PROMPT

    else:

        system_prompt = WOMEN_PROMPT


    # SEARCH TOOL
    tools = []

    if allow_search:

        tools = [
            TavilySearchResults(
                max_results=2
            )
        ]


    # CREATE AGENT
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )


    # USER MESSAGE
    state = {
        "messages": query
    }


    # RUN AGENT
    response = agent.invoke(state)

    messages = response.get(
        "messages",
        []
    )


    ai_messages = [

        message.content

        for message in messages

        if isinstance(
            message,
            AIMessage
        )
    ]


    if len(ai_messages) == 0:

        return "I'm here with you. Could you tell me a little more?"


    return ai_messages[-1]