# from dotenv import load_dotenv
# load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

from ai_agent import get_response_from_ai_agent
from database import (
    save_message,
    get_history
)

app = FastAPI(
    title="Mayi Disha"
)


# ==========================
# CHAT REQUEST
# ==========================

class ChatRequest(BaseModel):

    user_id: int

    session_id: str

    model_name: str

    support_type: str

    messages: List[str]

    allow_search: bool = False


# ==========================
# HOME ROUTE
# ==========================

@app.get("/")

def home():

    return {

        "message":
        "Mayi Disha Backend Running"

    }


# ==========================
# CHAT ROUTE
# ==========================

@app.post("/chat")

def chat(

    request: ChatRequest

):

    history = get_history(

        request.session_id

    )


    full_query = "\n".join(

        history +

        request.messages

    )


    response = get_response_from_ai_agent(

        request.model_name,

        full_query,

        request.allow_search,

        request.support_type

    )


    save_message(

        request.user_id,

        request.session_id,

        "user",

        request.messages[-1]

    )


    save_message(

        request.user_id,

        request.session_id,

        "assistant",

        response

    )


    return {

        "success": True,

        "response": response

    }


# ==========================
# RUN
# ==========================

import os

if __name__=="__main__":

    port = int(
        os.environ.get(
            "PORT",
            9999
        )
    )

    uvicorn.run(

        app,

        host="0.0.0.0",

        port=port

    )