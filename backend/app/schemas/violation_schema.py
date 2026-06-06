from datetime import datetime

from pydantic import BaseModel


class ViolationOut(BaseModel):
    violation_id: int
    car_id: int
    report_id: int | None = None
    report_time: datetime
    has_appealed: bool

    class Config:
        from_attributes = True


class ViolationDetailOut(ViolationOut):
    license_plate: str
    full_address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    photo_url: str | None = None
