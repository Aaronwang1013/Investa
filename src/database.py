from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.engine import URL

from src.config import settings


def _conntection_url() -> str:
    return URL.create(
        drivername="mysql+aiomysql",
        host=settings.DB_HOST,
        username=settings.MYSQL_DB_USER,
        password=settings.MYSQL_DB_PASSWORD,
        database=settings.MYSQL_DB_NAME,
        port=settings.DB_PORT,
    )


engine: AsyncEngine = create_async_engine(
    _conntection_url(),
    echo=settings.APP_DEBUG,
    future=True,
    pool_size=20,
    pool_recycle=3600,
)


AsessionSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsessionSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
