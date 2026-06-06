from datetime import datetime
from pydantic import BaseModel 


class ReportOut(BaseModel):
    report_id: int
    license_plate: str
    report_time: datetime
    full_address: str
    latitude: float | None = None
    longitude: float | None = None

    class Config:
        from_attributes = True

class ReportResponse(BaseModel):
    report_id: int
    license_plate: str
    report_time: datetime
    full_address: str
    latitude: float | None = None
    longitude: float | None = None
    photo_url: str | None = None
    photo_data: bytes | None = None  # 儲存圖片的二進位資料
    model_config = {
        "from_attributes": True
    }