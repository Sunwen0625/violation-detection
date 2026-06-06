from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.car_repository import CarRepository
from app.repositories.user_repository import UserRepository
from app.schemas.car_schema import CarCreate, CarOut


router = APIRouter(prefix="/api/cars", tags=["Cars"])


@router.get("/{user_id}", response_model=list[CarOut])
def get_user_cars(
    user_id: int,
    db: Session = Depends(get_db),
):
    user_repo = UserRepository(db)
    car_repo = CarRepository(db)

    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return car_repo.get_by_user(user_id)


@router.post("/{user_id}", response_model=CarOut)
def add_car(
    user_id: int,
    data: CarCreate,
    db: Session = Depends(get_db),
):
    user_repo = UserRepository(db)
    car_repo = CarRepository(db)

    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    license_plate = data.license_plate.upper()
    existing_cars = car_repo.get_by_user(user_id)
    for car in existing_cars:
        if car.license_plate == license_plate:
            raise HTTPException(status_code=400, detail="Car already exists")

    return car_repo.create(
        user_id=user_id,
        license_plate=license_plate,
    )


@router.delete("/{user_id}/{car_id}")
def delete_car(
    user_id: int,
    car_id: int,
    db: Session = Depends(get_db),
):
    car_repo = CarRepository(db)

    success = car_repo.delete(car_id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Car not found")

    return {"message": "deleted"}
