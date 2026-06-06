from pydantic import BaseModel

class CarOut(BaseModel):
    car_id: int
    license_plate: str

    class Config:
        from_attributes = True

class CarCreate(BaseModel):
    license_plate: str