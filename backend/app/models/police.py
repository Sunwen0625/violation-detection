from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.core.database import Base


class Police(Base):
    __tablename__ = "police"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    badge_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
    String,
    nullable=False,
    )   
    photo: Mapped[str | None] = mapped_column(String, nullable=True)

    appeals = relationship("Appeal", back_populates="police")
