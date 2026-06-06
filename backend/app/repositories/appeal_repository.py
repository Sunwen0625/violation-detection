from sqlalchemy.orm import Session

from app.models.appeals import Appeal


class AppealRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        violation_id: int,
        police_id: int,
        appeal_reason: str,
        status: str = "pending",
    ) -> Appeal:
        appeal = Appeal(
            violation_id=violation_id,
            police_id=police_id,
            appeal_reason=appeal_reason,
            status=status,
        )
        self.db.add(appeal)
        self.db.commit()
        self.db.refresh(appeal)
        return appeal

    def get_by_id(self, appeal_id: int) -> Appeal | None:
        return (
            self.db.query(Appeal)
            .filter(Appeal.appeal_id == appeal_id)
            .first()
        )

    def get_by_violation(self, violation_id: int) -> Appeal | None:
        return (
            self.db.query(Appeal)
            .filter(Appeal.violation_id == violation_id)
            .first()
        )

    def get_all(self) -> list[Appeal]:
        return self.db.query(Appeal).order_by(Appeal.appeal_id.desc()).all()

    def get_by_police(self, police_id: int) -> list[Appeal]:
        return (
            self.db.query(Appeal)
            .filter(Appeal.police_id == police_id)
            .order_by(Appeal.appeal_id.desc())
            .all()
        )

    def update_status(self, appeal_id: int, status: str) -> Appeal | None:
        appeal = self.get_by_id(appeal_id)
        if not appeal:
            return None

        appeal.status = status
        self.db.commit()
        self.db.refresh(appeal)
        return appeal
