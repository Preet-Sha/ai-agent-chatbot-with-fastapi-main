from langchain_groq import ChatGroq

from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent

from langchain_core.messages.ai import AIMessage


CHILD_PROMPT = """
You are an emotional support AI for children.

Be gentle.

Use simple language.

Encourage trusted adults.

Prioritize safety.
"""


WOMEN_PROMPT = """
You are an emotional support AI for women.

Be supportive.

Never judge.

Prioritize safety.
"""


def get_response_from_ai_agent(

    model,

    query,

    allow_search,

    support_type

):

    llm = ChatGroq(
        model=model
    )


    if support_type == "child":

        prompt = CHILD_PROMPT

    else:

        prompt = WOMEN_PROMPT


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

        state_modifier=prompt
    )


    response = agent.invoke(

        {

            "messages":query

        }
    )


    messages = response[
        "messages"
    ]


    ai = [

        x.content

        for x in messages

        if isinstance(
            x,
            AIMessage
        )

    ]


    return ai[-1]