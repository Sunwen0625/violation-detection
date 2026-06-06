from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Appeal(Base):
    __tablename__ = "appeals"

    appeal_id: Mapped[int] = mapped_column(primary_key=True)

    violation_id: Mapped[int] = mapped_column(
        ForeignKey("violations.violation_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    police_id: Mapped[int] = mapped_column(
        ForeignKey("police.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(String, nullable=False)
    appeal_reason: Mapped[str | None] = mapped_column(Text)

    police = relationship("Police", back_populates="appeals")
    violation = relationship("Violation", back_populates="appeal")
