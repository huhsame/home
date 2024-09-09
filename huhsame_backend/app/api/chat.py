from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.langchain_service import langchain_service

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
async def chat_endpoint(user_message: ChatMessage):
    try:
        response = await langchain_service.get_response(user_message.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/history")
async def chat_history():
    try:
        history = await langchain_service.get_chat_history()
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
