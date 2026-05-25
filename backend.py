from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from ai_agent import get_response_from_ai_agent

from database import (
    create_user,
    login_user,
    save_message,
    get_history
)

app = FastAPI(
    title="Safe Support Chatbot"
)


class SignupRequest(BaseModel):

    name:str

    email:str

    password:str

    support_type:str


class LoginRequest(BaseModel):

    email:str

    password:str


class ChatRequest(BaseModel):

    user_id:int

    session_id:str

    model_name:str

    model_provider:str

    support_type:str

    messages:List[str]

    allow_search:bool



@app.post("/signup")
def signup(
    request:SignupRequest
):

    success = create_user(

        request.name,

        request.email,

        request.password,

        request.support_type
    )

    if success:

        return {

            "success":True,

            "message":"Account created"

        }

    return {

        "success":False,

        "message":"Email already exists"

    }



@app.post("/login")
def login(
    request:LoginRequest
):

    user = login_user(

        request.email,

        request.password
    )


    if user is None:

        return {

            "success":False,

            "message":"Invalid credentials"

        }


    return {

        "success":True,

        "user_id":user[0],

        "name":user[1],

        "support_type":user[2]

    }



@app.post("/chat")
def chat(
    request:ChatRequest
):

    history = get_history(
        request.session_id
    )

    full_query = (

        history +

        request.messages
    )


    response = get_response_from_ai_agent(

        request.model_name,

        full_query,

        request.allow_search,

        request.model_provider,

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

        "success":True,

        "response":response

    }



if __name__=="__main__":

    import uvicorn

    uvicorn.run(

        app,

        host="127.0.0.1",

        port=9999,

        reload=True
    )