from pydantic import BaseModel


class AppealCreate(BaseModel):
    violation_id: int
    police_id: int
    appeal_reason: str


class AppealStatusUpdate(BaseModel):
    status: str


class AppealOut(BaseModel):
    appeal_id: int
    violation_id: int
    police_id: int
    status: str
    appeal_reason: str | None = None

    class Config:
        from_attributes = True
