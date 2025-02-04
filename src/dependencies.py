from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_db() -> AsyncSession:
    from src.database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
