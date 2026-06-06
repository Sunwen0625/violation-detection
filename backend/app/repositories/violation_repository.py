from sqlalchemy.orm import Session
from app.models.violation import Violation
from app.models.cars import Car


class ViolationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        car_id: int,
        report_id: int | None = None,
    ) -> Violation:
        violation = Violation(
            car_id=car_id,
            report_id=report_id,
    
        )
        self.db.add(violation)
        self.db.commit()
        self.db.refresh(violation)
        return violation

    def get_by_id(self, violation_id: int) -> Violation | None:
        return (
            self.db.query(Violation)
            .filter(Violation.violation_id == violation_id)
            .first()
        )

    def get_all(self) -> list[Violation]:
        return (
            self.db.query(Violation)
            .order_by(Violation.report_time.desc())
            .all()
        )

    def get_by_user(self, user_id: int) -> list[Violation]:
        return (
            self.db.query(Violation)
            .join(Car, Violation.car_id == Car.car_id)
            .filter(Car.user_id == user_id)
            .order_by(Violation.report_time.desc())
            .all()
        )

    def mark_appealed(self, violation_id: int) -> Violation | None:
        violation = self.get_by_id(violation_id)
        if not violation:
            return None

        violation.has_appealed = True
        self.db.commit()
        self.db.refresh(violation)
        return violation
