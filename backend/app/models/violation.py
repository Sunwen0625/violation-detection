from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Violation(Base):
    __tablename__ = "violations"

    violation_id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(
        ForeignKey("cars.car_id", ondelete="CASCADE"),
        nullable=False,
    )
    report_id: Mapped[int | None] = mapped_column(
        ForeignKey("reports.report_id", ondelete="SET NULL"),
        nullable=True,
    )
    report_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )
    has_appealed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    car = relationship("Car", back_populates="violations")
    report = relationship("Report", back_populates="violations")
    appeal = relationship("Appeal", back_populates="violation", uselist=False)
