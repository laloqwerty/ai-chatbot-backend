from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.chat import ChatRequest
from app.services.chat_service import chat_chain


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    response = chat_chain.invoke(
        {"message": request.message},
        config={"configurable": {"session_id": request.session_id}},
    )
    return {"reply": response.content}


@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    def generate():
        for chunk in chat_chain.stream(
            {"message": request.message},
            config={"configurable": {"session_id": request.session_id}},
        ):
            if chunk.content:
                yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")