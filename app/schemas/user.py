from pydantic import BaseModel, EmailStr, field_validator
import re
from app.core.errors import AppError


class UserCreate(BaseModel):
    email: EmailStr
    mobile_number: str
    password: str

    @field_validator("mobile_number")
    def validate_mobile_number(cls, mobile_number: str) -> str:
        mobile_number = mobile_number.strip()
        if not mobile_number.isdigit():
            raise AppError("Invalid mobile number")
        if len(mobile_number) != 10:
            raise AppError("Invalid mobile number")
        return mobile_number

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise AppError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", password):
            raise AppError("password must contain at least one uppercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise AppError("password must contain at least one special character")
        return password

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    mobile_number: str
    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

