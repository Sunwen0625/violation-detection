from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime

from app.dependencies.database import get_db
from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import  ReportResponse, ReportOut



router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post("/upload")
async def upload_report(
    license_plate: str = Form(...),
    full_address: str = Form(...),
    latitude: float | None = Form(None),
    longitude: float | None = Form(None),
    file: UploadFile | None = File(None),      # 上傳圖片
    photo_url: str | None = Form(None),        # 或 URL

    db: Session = Depends(get_db),
):
    repo = ReportRepository(db)

    # ❗ 互斥檢查
    if file and photo_url:
        raise HTTPException(400, "Only one of file or photo_url allowed")

    photo_data = None
    photo_content_type = None

    # ✔ case 1：file upload
    if file:
        if not file.content_type.startswith("image/"):
            raise HTTPException(400, "File must be image")
        
        photo_data = await file.read()
        photo_content_type = file.content_type

    # ✔ case 2：URL
    elif photo_url:
        photo_data = None
        photo_content_type = None

    #杜絕短時間內重複舉報同一車牌
    #if repo.exists_recent(payload.license_plate):
        #raise HTTPException(400, "Duplicate report in short time")

    report = repo.create(
        license_plate=license_plate,
        report_time=datetime.now(),
        full_address=full_address,
        latitude=latitude,
        longitude=longitude,
        photo_url=photo_url,
        photo_data=photo_data,
        photo_content_type=photo_content_type,
    )

    return {
        "report_id": report.report_id,
        "message": "upload success"
    }

@router.get("/", response_model=list[ReportOut])
def get_reports(db: Session = Depends(get_db)):
    repo = ReportRepository(db)

    return repo.get_all()


@router.get("/{report_id}/image")
def get_report_image(report_id: int, db: Session = Depends(get_db)):
    repo = ReportRepository(db)

    report = repo.get_by_id(report_id)

    if not report or not report.photo_data:
        raise HTTPException(404, "Image not found")

    return Response(
            content=report.photo_data,
            media_type=report.photo_content_type or "image/jpeg"
        )