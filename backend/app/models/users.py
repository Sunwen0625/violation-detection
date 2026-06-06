from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.core.database import Base
from datetime import datetime


class User(Base):

    """
    User类，表示用户实体，继承自Base类
    使用SQLAlchemy ORM映射到数据库表
    """
    __tablename__ = "users"  # 指定对应的数据库表名为"users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(
    String,
    nullable=False,
    )
    id_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    photo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    

    cars = relationship(
        "Car",
        back_populates="user",
        cascade="all, delete-orphan",
    )
