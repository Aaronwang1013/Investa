from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_db() -> AsyncSession:
    from src.database import LocalSession

    async with LocalSession() as session:
        yield session
