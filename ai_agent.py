from langchain_groq import ChatGroq

from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent

from langchain_core.messages import HumanMessage

from langchain_core.messages.ai import AIMessage

from langchain.memory import ConversationBufferMemory


# ==========================
# MEMORY
# ==========================

memory = ConversationBufferMemory(

    return_messages=True

)


# ==========================
# CRISIS DETECTION
# ==========================

CRISIS_WORDS = [

    "hurt myself",

    "kill myself",

    "suicide",

    "end my life",

    "self harm",

    "want to die",

    "die"

]


EMERGENCY_RESPONSE = """

I'm really sorry you're going through this.

Please talk to someone you trust immediately.

You deserve support and help 🌸

Consider reaching out to local emergency or crisis services.

"""


def detect_crisis(

    text

):

    text = text.lower()


    for word in CRISIS_WORDS:

        if word in text:

            return True

    return False


# ==========================
# CHILD PROMPT
# ==========================

CHILD_PROMPT = """

You are an emotional support AI for children.

Rules:

- Keep response short

- Maximum 2-3 lines

- Use simple language

- Be gentle

- Encourage trusted adults

- Prioritize safety

Reply in less than 50 words.

"""


# ==========================
# WOMEN PROMPT
# ==========================

WOMEN_PROMPT = """

You are an emotional support AI for women.

Rules:

- Keep responses concise

- Maximum 2-4 lines

- Be supportive

- Never judge

- Prioritize safety

Reply in less than 50 words.

"""


# ==========================
# MAIN FUNCTION
# ==========================

def get_response_from_ai_agent(

    model,

    query,

    allow_search,

    support_type

):


    # ------------------
    # CRISIS CHECK
    # ------------------

    if detect_crisis(

        query

    ):

        return EMERGENCY_RESPONSE


    llm = ChatGroq(

        model=model,

        temperature=0.3,

        max_tokens=120

    )


    prompt = (

        CHILD_PROMPT

        if support_type=="child"

        else WOMEN_PROMPT

    )


    tools=[]


    if allow_search:

        tools=[

            TavilySearchResults(

                max_results=2

            )

        ]


    agent = create_react_agent(

        model=llm,

        tools=tools,

        state_modifier=prompt

    )


    # ------------------
    # MEMORY LOAD
    # ------------------

    history = memory.load_memory_variables(

        {}

    )


    past = history.get(

        "history",

        []

    )


    all_messages = past + [

        HumanMessage(

            content=query

        )

    ]


    response = agent.invoke(

        {

            "messages":

            all_messages

        }

    )


    messages = response[

        "messages"

    ]


    ai_messages = [

        x.content

        for x in messages

        if isinstance(

            x,

            AIMessage

        )

    ]


    final_response = ai_messages[-1]


    # ------------------
    # SAVE MEMORY
    # ------------------

    memory.save_context(

        {

            "input":

            query

        },

        {

            "output":

            final_response

        }

    )


    return final_response