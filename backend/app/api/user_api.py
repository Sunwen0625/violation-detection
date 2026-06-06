from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdateSchema


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    existing_user = repo.get_by_email(payload.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    return repo.create(
        name=payload.name,
        email=payload.email,
        hashed_password=payload.hashed_password,
        phone_number=payload.phone_number,
        address=payload.address,
        id_number=payload.id_number,
        photo_url=payload.photo_url,
    )

@router.get("/by-email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_email(email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "name": user.name,
        "email": user.email,
        "phone": user.phone_number,
        "idNumber": user.id_number,
        "address": user.address,
        "avatar": user.photo_url,
    }

@router.put("/by-email/{email}")
def update_user_by_email(
    email: str,
    payload: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    updated_user = repo.update_by_email(
        email,
        {
            "name": payload.name,
            "email": payload.email,
            "phone_number": payload.phone_number,
            "address": payload.address,
            "id_number": payload.id_number,
            "photo_url": payload.photo_url,
        },
    )

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "更新成功",
        "user": {
            "name": updated_user.name,
            "email": updated_user.email,
            "phone": updated_user.phone_number,
            "idNumber": updated_user.id_number,
            "address": updated_user.address,
            "avatar": updated_user.photo_url,
        },
    }
