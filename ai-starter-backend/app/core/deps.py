from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import verify_token
from app.db.database import get_db
from app.models.models import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get the current authenticated user."""
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
