from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Car(Base):

    """
    Car类，表示汽车信息，继承自Base类。
    使用SQLAlchemy ORM映射到数据库表。
    """
    __tablename__ = "cars"  # 指定数据库表名为"cars"

    car_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    license_plate: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    user = relationship("User", back_populates="cars")
    violations = relationship(
        "Violation",
        back_populates="car",
        cascade="all, delete-orphan",
    )
