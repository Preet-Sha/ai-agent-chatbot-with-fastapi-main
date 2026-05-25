from langchain_groq import ChatGroq

from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent

from langchain_core.messages.ai import AIMessage

CHILD_PROMPT = """
You are an emotional support AI for children.

Rules:

- Keep responses short (2-3 lines max)
- Use simple words
- Be gentle
- Encourage trusted adults
- Prioritize safety

Do not give long explanations.
"""

WOMEN_PROMPT = """
You are an emotional support AI for women.

Rules:

- Keep responses concise (2-4 lines max)
- Be supportive
- Never judge
- Prioritize safety

Avoid long paragraphs.
"""

def get_response_from_ai_agent(

    model,

    query,

    allow_search,

    support_type

):

    llm = ChatGroq(
    model=model,
    temperature=0.3,
    max_tokens=120
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