import os
from dotenv import load_dotenv

from pydantic import BaseModel
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import marvin

import uvicorn


# Load environment variables
load_dotenv()


# Define the CORS origins that are allowed to access your API
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://dev.project-exterior.com",
    "https://project-exterior.com"
]

OPEN_AI_API_KEY=os.environ.get('OPEN_AI_API_KEY')
print(OPEN_AI_API_KEY)

marvin.settings.openai.api_key = os.environ.get('OPEN_AI_API_KEY')

app = FastAPI()

# Add the CORS middleware to app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex='https://project-exterior-.*\.vercel\.app',
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@marvin.ai_fn
def create_response_user_question(body: Dict) -> str:
    """
    Given `body.readable_context_data`, and supported by raw context data in `body.context_data`, create response to the question in `body.question`.
    """

@marvin.ai_fn
def summarize_conversation(body: Dict) -> str:
    """
    Given chat history in `body.chat_data.message_list`, create a summary, with maximum 300 characters.
    """

@marvin.ai_fn
def create_reply_chat(body: Dict) -> str:
    """
    Given chat history in `body.chat_data.message_list`, context in `body.readable_context_data`, supported by raw context data in `body.context_data`, create reply representing @wisatajawa helpdesk team.
    """


@marvin.ai_model
class EmailDraft(BaseModel):
    subject: str;
    body: str;
    
@marvin.ai_fn
def create_email_draft(body: Dict) -> EmailDraft:
    # Prompt still resulting bad result
    """
    We are a helpdesk team of travel company, we need to make `body.email_subject` request to the hotel by an email.
    Please create an email draft with proper subject and compact understandable body. Use HTML format for the body.
    Here's the data regarding the email and the request:
    from=helpdesk@wisatajawa
    to=support@ascott.hotel
    booker_name=`body.context_data.owner_data.name`
    `body.email_body_type`=`body.email_body_text`
    booking_data=`body.readable_context_data`
    """

@app.post('/question')
async def response_user_question(request: Request) -> str:
    try:
        body = await request.json()
        result = create_response_user_question(body=body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail={ 'detail': str(e) })


@app.post('/summarize')
async def create_summarize_conversation(request: Request) -> str:
    try:
        body = await request.json()
        # result = summarize_conversation(body=body)
        result = summarize_conversation(body=body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail={ 'detail': str(e) })
    

@app.post('/reply')
async def reply_chat(request: Request) -> str:
    try:
        body = await request.json()
        result = create_reply_chat(body=body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail={ 'detail': str(e) })

    
@app.post('/email')
async def email_draft(request: Request):
    try:
        body = await request.json()
        result = create_email_draft(body=body)
        return result.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail={ 'detail': str(e) })
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)