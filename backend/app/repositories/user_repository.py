from sqlalchemy.orm import Session
from app.models.users import User


class UserRepository:
    """
    專門處理 users table 的資料操作
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        email: str,
        hashed_password: str,
        phone_number: str,
        address: str,
        id_number: str,
        photo_url: str | None = None,
    ) -> User:
        user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            phone_number=phone_number,
            address=address,
            id_number=id_number,
            photo_url=photo_url,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).all()
    
    def update_by_email(self, email: str, data: dict) -> User | None:
        user = self.get_by_email(email)
        if not user:
            return None

        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True
