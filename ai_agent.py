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
# CHILD PROMPT
# ==========================

CHILD_PROMPT = """

You are an emotional support AI for children.

Rules:

- Keep responses short

- Maximum 2 lines

- Use simple words

- Be gentle

- Encourage trusted adults

Reply under 40 words.

"""


# ==========================
# WOMEN PROMPT
# ==========================

WOMEN_PROMPT = """

You are an emotional support AI for women.

Rules:

- Keep responses concise

- Maximum 3 lines

- Be supportive

- Never judge

Reply under 50 words.

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


    current_message = query.split(
        "\n"
    )[-1]


    llm = ChatGroq(

        model=model,

        temperature=0.3,

        max_tokens=100

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


    # LOAD MEMORY

    history = memory.load_memory_variables(
        {}
    )


    past = history.get(

        "history",

        []

    )


    all_messages = past + [

        HumanMessage(

            content=current_message

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


    # SAVE MEMORY

    memory.save_context(

        {

            "input":

            current_message

        },

        {

            "output":

            final_response

        }

    )


    return final_response