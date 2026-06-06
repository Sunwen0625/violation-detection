from sqlalchemy.orm import Session
from app.models.cars import Car


class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        license_plate: str,
    ) -> Car:
        car = Car(
            user_id=user_id,
            license_plate=license_plate,
        )
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)
        return car

    def get_by_plate(self, plate: str) -> Car | None:
        return (
            self.db.query(Car)
            .filter(Car.license_plate == plate)
            .first()
        )

    def get_by_user(self, user_id: int) -> list[Car]:
        return self.db.query(Car).filter(Car.user_id == user_id).all()
    
    def delete(self, car_id: int, user_id: int) -> bool:
        car = (
            self.db.query(Car)
            .filter(Car.car_id == car_id, Car.user_id == user_id)
            .first()
        )

        if not car:
            return False

        self.db.delete(car)
        self.db.commit()
        return True
