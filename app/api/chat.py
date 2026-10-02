from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.requests import ChatRequest
from app.schemas.chat import ChatResponse
from app.services.chat_service import chat

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    try:
        reply = chat(
            db=db,
            message=request.message,
            language=request.language,
        )

        return ChatResponse(
            reply=reply,
            session_id=request.session_id,
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )