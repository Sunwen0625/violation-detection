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


def ensure_database_objects() -> None:
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE reports ALTER COLUMN latitude DROP NOT NULL"))
        conn.execute(text("ALTER TABLE reports ALTER COLUMN longitude DROP NOT NULL"))
        conn.execute(text("""
            CREATE OR REPLACE FUNCTION create_violation_from_report()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO violations (car_id, report_id, report_time, has_appealed)
                SELECT car_id, NEW.report_id, NEW.report_time, FALSE
                FROM cars
                WHERE UPPER(license_plate) = UPPER(NEW.license_plate)
                ON CONFLICT DO NOTHING;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """))
        conn.execute(text("""
            DROP TRIGGER IF EXISTS reports_after_insert_create_violation ON reports;
        """))
        conn.execute(text("""
            CREATE TRIGGER reports_after_insert_create_violation
            AFTER INSERT ON reports
            FOR EACH ROW
            EXECUTE FUNCTION create_violation_from_report();
        """))

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
