from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent

from langchain_core.messages.ai import AIMessage


CHILD_PROMPT = """
You are a gentle emotional support assistant for children.

Use simple language.

Be supportive.

Encourage trusted adults.

Prioritize safety.
"""


WOMEN_PROMPT = """
You are a trauma informed support assistant for women.

Be warm.

Never judge.

Validate emotions.

Prioritize safety.
"""


def get_response_from_ai_agent(

    llm_id,

    query,

    allow_search,

    provider,

    support_type

):

    llm = ChatGroq(
        model=llm_id
    )


    if support_type == "child":

        system_prompt = CHILD_PROMPT

    else:

        system_prompt = WOMEN_PROMPT


    tools = []

    if allow_search:

        tools = [

            TavilySearchResults(
                max_results=2
            )

        ]


    agent = create_react_agent(

        model=llm,

        tools=tools,

        state_modifier=system_prompt
    )


    response = agent.invoke(

        {
            "messages": query
        }
    )


    messages = response.get(
        "messages",
        []
    )


    ai_messages = [

        msg.content

        for msg in messages

        if isinstance(
            msg,
            AIMessage
        )

    ]


    return ai_messages[-1]