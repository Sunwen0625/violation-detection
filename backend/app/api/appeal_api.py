from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.appeal_repository import AppealRepository
from app.repositories.police_repository import PoliceRepository
from app.repositories.violation_repository import ViolationRepository
from app.schemas.appeal_schema import AppealCreate, AppealOut, AppealStatusUpdate


router = APIRouter(prefix="/api/appeals", tags=["Appeals"])

ALLOWED_STATUSES = {"pending", "approved", "rejected"}


@router.post("/", response_model=AppealOut)
def create_appeal(payload: AppealCreate, db: Session = Depends(get_db)):
    appeal_repo = AppealRepository(db)
    police_repo = PoliceRepository(db)
    violation_repo = ViolationRepository(db)

    violation = violation_repo.get_by_id(payload.violation_id)
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    police = police_repo.get_by_id(payload.police_id)
    if not police:
        raise HTTPException(status_code=404, detail="Police not found")

    if appeal_repo.get_by_violation(payload.violation_id):
        raise HTTPException(status_code=400, detail="Violation already appealed")

    appeal = appeal_repo.create(
        violation_id=payload.violation_id,
        police_id=payload.police_id,
        appeal_reason=payload.appeal_reason,
    )
    violation_repo.mark_appealed(payload.violation_id)
    return appeal


@router.get("/", response_model=list[AppealOut])
def get_appeals(db: Session = Depends(get_db)):
    repo = AppealRepository(db)
    return repo.get_all()


@router.get("/police/{police_id}", response_model=list[AppealOut])
def get_police_appeals(police_id: int, db: Session = Depends(get_db)):
    police_repo = PoliceRepository(db)
    appeal_repo = AppealRepository(db)

    police = police_repo.get_by_id(police_id)
    if not police:
        raise HTTPException(status_code=404, detail="Police not found")

    return appeal_repo.get_by_police(police_id)


@router.patch("/{appeal_id}/status", response_model=AppealOut)
def update_appeal_status(
    appeal_id: int,
    payload: AppealStatusUpdate,
    db: Session = Depends(get_db),
):
    status = payload.status.lower()
    if status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Status must be pending, approved, or rejected",
        )

    repo = AppealRepository(db)
    appeal = repo.update_status(appeal_id, status)
    if not appeal:
        raise HTTPException(status_code=404, detail="Appeal not found")

    return appeal
