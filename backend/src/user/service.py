from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import User
from src.auth.request import RegisterRequest
from src.dependencies import password_context
from fastapi import HTTPException, status


class UserService:
    def __init__(self):
        pass

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def create_user(request: RegisterRequest, session: AsyncSession) -> User:
        hashed_password = password_context.hash(request.password)
        new_user = User(
            username=request.username, email=request.email, password=hashed_password
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def create_oauth_user(
        email: str, username: str, session: AsyncSession
    ) -> User:
        new_user = User(
            username=username,
            email=email,
            password=None,
            is_active=True,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def update_user_password(
        session: AsyncSession, email: str, new_password: str
    ):
        user = await UserService.get_user_by_email(session, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user.password = password_context.hash(new_password)
        await session.commit()
        await session.refresh(user)
        return user
