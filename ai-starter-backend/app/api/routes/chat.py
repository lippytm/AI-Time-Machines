from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from openai import OpenAI

from app.db.database import get_db
from app.models.models import User, Message
from app.models.schemas import ChatRequest, ChatResponse
from app.core.deps import get_current_user
from app.core.config import settings

router = APIRouter()


def local_model_stub(messages: list[dict]) -> str:
    """
    Local model stub for development.
    Simply echoes back the last user message.
    """
    if messages:
        last_message = messages[-1]["content"]
        return f"Echo (local model): {last_message}"
    return "Echo (local model): No message received"


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Chat endpoint that forwards messages to OpenAI or uses local stub.
    Stores messages in the database.
    """
    # Convert request messages to dict format
    messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    # Store user message
    if messages_dict:
        last_user_msg = next((m for m in reversed(messages_dict) if m["role"] == "user"), None)
        if last_user_msg:
            user_message = Message(
                user_id=current_user.id,
                role="user",
                content=last_user_msg["content"]
            )
            db.add(user_message)
    
    # Generate response
    if settings.USE_LOCAL_MODEL or not settings.OPENAI_API_KEY:
        # Use local model stub
        response_content = local_model_stub(messages_dict)
    else:
        # Use OpenAI
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            completion = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages_dict
            )
            response_content = completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    
    # Store assistant response
    assistant_message = Message(
        user_id=current_user.id,
        role="assistant",
        content=response_content
    )
    db.add(assistant_message)
    
    await db.commit()
    
    return ChatResponse(role="assistant", content=response_content)
