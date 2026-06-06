from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    phone_number: str
    address: str
    id_number: str
    photo_url: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    address: str
    id_number: str
    photo_url: str | None = None

    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    name: str | None 
    email: str | None 
    phone_number: str | None 
    address: str | None 
    id_number: str | None
    photo_url: str | None = None
