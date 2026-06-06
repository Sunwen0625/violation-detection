from pydantic import BaseModel


class PoliceCreate(BaseModel):
    name: str
    badge_number: str
    hashed_password: str
    photo: str | None = None


class PoliceResponse(BaseModel):
    id: int
    name: str
    badge_number: str
    photo: str | None = None

    class Config:
        from_attributes = True
