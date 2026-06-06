from datetime import datetime , timedelta
from sqlalchemy.orm import Session
from app.models.reports import Report

class ReportRepository:
    def __init__(self, db: Session):
        """
        初始化方法，接收数据库会话作为参数
        Args:
            db: 数据库会话对象
        """
        self.db = db

    def get_by_license_plate(self, license_plate: str):
        return (
            self.db.query(Report)
            .filter(Report.license_plate == license_plate)
            .first()
        )
    
    def exists_recent(self, license_plate: str, minutes: int = 5):
        return (
            self.db.query(Report)
            .filter(
                Report.license_plate == license_plate,
                Report.report_time >= datetime.now() - timedelta(minutes=minutes)
            )
            .first()
        )
    
    def get_by_id(self, report_id: int) -> Report | None:
        return (
            self.db.query(Report)
            .filter(Report.report_id == report_id)
            .first()
        )
    
    def get_all(self):
        return (
            self.db.query(Report)
            .order_by(Report.report_time.desc())
            .all()
        )

    def create(
        self,
        license_plate: str,          # 车牌号，字符串类型
        report_time: datetime,        # 报告时间，datetime类型
        full_address: str,            # 完整地址，字符串类型
        latitude: float | None,       # 纬度，浮点类型或None
        longitude: float | None,      # 经度，浮点类型或None
        photo_url: str | None,        # 照片链接，字符串类型或None
        photo_data: bytes | None,
        photo_content_type: str | None,  # 照片内容类型，字符串类型或None
    ) -> Report:                     # 返回Report类型的对象

        # 创建一个新的Report对象，使用传入的参数
        report = Report(
            license_plate=license_plate,
            report_time=report_time,
            full_address=full_address,
            latitude=latitude,
            longitude=longitude,
            photo_url=photo_url,
            photo_data=photo_data,
            photo_content_type=photo_content_type,
        )

        # 将新报告添加到数据库
        self.db.add(report)
        # 提交数据库事务
        self.db.commit()
        # 刷新报告对象，确保获取到数据库中的最新数据
        self.db.refresh(report)

        # 返回创建的报告对象
        return report