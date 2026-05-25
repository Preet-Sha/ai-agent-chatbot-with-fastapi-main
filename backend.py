# # Uncomment if not using pipenv
# from dotenv import load_dotenv
# load_dotenv()

# ==========================
# STEP 1: SCHEMA
# ==========================
from pydantic import BaseModel
from typing import List


class RequestState(BaseModel):

    model_name: str

    model_provider: str

    support_type: str

    messages: List[str]

    allow_search: bool


# ==========================
# STEP 2: IMPORTS
# ==========================
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent


app = FastAPI(
    title="Abuse Support Chatbot"
)


# ALLOWED MODELS
ALLOWED_MODEL_NAMES = [

    "llama3-70b-8192",

    "mixtral-8x7b-32768",

    "llama-3.3-70b-versatile",

    "gpt-4o-mini"
]


# ==========================
# CHAT ENDPOINT
# ==========================
@app.post("/chat")
async def chat_endpoint(
    request: RequestState
):

    try:

        if request.model_name not in ALLOWED_MODEL_NAMES:

            return {
                "status": "error",

                "message":
                "Invalid model selected"
            }


        response = get_response_from_ai_agent(

            llm_id=request.model_name,

            query=request.messages,

            allow_search=request.allow_search,

            provider=request.model_provider,

            support_type=request.support_type

        )


        return {

            "status": "success",

            "response": response

        }


    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }


# ==========================
# RUN APP
# ==========================
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend:app",

        host="127.0.0.1",

        port=9999,

        reload=True
    )