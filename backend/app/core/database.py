import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, echo=True)


def test_db_connection() -> str:
    """
    測試資料庫連線是否正常
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return f"success: {result.scalar()}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)