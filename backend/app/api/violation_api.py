from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.violation_repository import ViolationRepository
from app.schemas.violation_schema import ViolationDetailOut, ViolationOut


router = APIRouter(prefix="/api/violations", tags=["Violations"])


def to_detail(violation) -> ViolationDetailOut:
    report = violation.report
    return ViolationDetailOut(
        violation_id=violation.violation_id,
        car_id=violation.car_id,
        report_id=violation.report_id,
        report_time=violation.report_time,
        has_appealed=violation.has_appealed,
        license_plate=violation.car.license_plate,
        full_address=report.full_address if report else None,
        latitude=report.latitude if report else None,
        longitude=report.longitude if report else None,
        photo_url=report.photo_url if report else None,
    )


@router.get("/", response_model=list[ViolationOut])
def get_violations(db: Session = Depends(get_db)):
    repo = ViolationRepository(db)
    return repo.get_all()


@router.get("/user/{user_id}", response_model=list[ViolationDetailOut])
def get_user_violations(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    violation_repo = ViolationRepository(db)

    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [to_detail(violation) for violation in violation_repo.get_by_user(user_id)]


@router.get("/{violation_id}", response_model=ViolationDetailOut)
def get_violation(violation_id: int, db: Session = Depends(get_db)):
    repo = ViolationRepository(db)
    violation = repo.get_by_id(violation_id)

    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    return to_detail(violation)
