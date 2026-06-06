from datetime import datetime
from sqlalchemy import String, DateTime, Numeric , LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Report(Base):
    __tablename__ = "reports"

    report_id: Mapped[int] = mapped_column(primary_key=True)
    license_plate: Mapped[str] = mapped_column(String, nullable=False)
    report_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.fromtimestamp(0),
    )
    full_address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float | None] = mapped_column(
    Numeric(9, 6),
    nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    photo_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    photo_data: Mapped[bytes | None] = mapped_column(
    LargeBinary,
    nullable=True
    )

    photo_content_type: Mapped[str | None] = mapped_column(
    String,
    nullable=True
)

    violations = relationship("Violation", back_populates="report")

