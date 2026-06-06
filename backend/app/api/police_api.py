from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.police_repository import PoliceRepository
from app.schemas.police_schema import (
    PoliceCreate,
    PoliceResponse,
)
from app.core.security import hash_password

router = APIRouter(prefix="/police", tags=["Police"])


@router.post("/register", response_model=PoliceResponse)
def register_police(
    payload: PoliceCreate,
    db: Session = Depends(get_db),
):
    repo = PoliceRepository(db)

    existing = repo.get_by_badge(payload.badge_number)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Badge number already exists",
        )

    return repo.create(
        name=payload.name,
        badge_number=payload.badge_number,
        hashed_password=hash_password(payload.hashed_password),
        photo=payload.photo,
    )
