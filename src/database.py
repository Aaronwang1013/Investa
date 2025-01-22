from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings


def _conntection_url() -> str:
    return URL.create(
        drivername="mysql+pymysql",
        host=settings.DB_HOST,
        username=settings.MYSQL_DB_USER,
        password=settings.MYSQL_DB_PASSWORD,
        database=settings.MYSQL_DB_NAME,
        port=settings.DB_PORT,
    )


engine = create_engine(
    _conntection_url(),
    echo=settings.APP_DEBUG,
    future=True,
    pool_size=20,
    pool_recycle=3600,
)


LocalSession = sessionmaker(bind=engine)

def get_db():
    db = LocalSession()

    try:
        yield db

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

