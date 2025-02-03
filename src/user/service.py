from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import User
from src.auth.request import LoginRequest, RegisterRequest
from src.dependencies import password_context



class UserService:
    def __init__(self):
        pass
    async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    
    async def create_user(request: RegisterRequest, session: AsyncSession) -> User:
        hashed_password = password_context.hash(request.password)
        new_user = User(
            username=request.username,
            email=request.email,
            password=hashed_password
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user 