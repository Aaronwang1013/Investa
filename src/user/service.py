from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import User
from src.user.schema import UserCreate
from src.dependencies import password_context



class UserService:
    def __init__(self):
        pass
    async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    
    async def create_user(session: AsyncSession, user: UserCreate) -> User:
        hashed_password = password_context.hash(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user