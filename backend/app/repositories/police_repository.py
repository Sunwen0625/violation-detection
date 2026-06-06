from sqlalchemy.orm import Session
from app.models.police import Police


class PoliceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        badge_number: str,
        hashed_password: str,
        photo: str | None = None,
    ) -> Police:
        police = Police(
            name=name,
            badge_number=badge_number,
            hashed_password=hashed_password,
            photo=photo,
        )
        self.db.add(police)
        self.db.commit()
        self.db.refresh(police)
        return police

    def get_by_badge(self, badge_number: str) -> Police | None:
        return (
            self.db.query(Police)
            .filter(Police.badge_number == badge_number)
            .first()
        )

    def get_by_id(self, police_id: int) -> Police | None:
        return (
            self.db.query(Police)
            .filter(Police.id == police_id)
            .first()
        )
