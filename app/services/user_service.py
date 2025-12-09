from datetime import datetime,timezone,timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.user import UserLogin
import jwt
from app.utils.hashing import hash_password, verify_password
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set")
ALGORITHM = os.getenv("ALGORITHM")
if not ALGORITHM:
    raise RuntimeError("ALGORITHM not set")
ACCESS_TOKEN_EXPIRY  =os.getenv("ACCESS_TOKEN_EXPIRY")
if not ACCESS_TOKEN_EXPIRY:
    raise RuntimeError("ACCESS_TOKEN_EXPIRY not set")

def create_user(email: str, mobile_number: str, password: str, db: Session):
    if db.query(User).filter(User.email == email).first():
        raise ValueError("Email already registered")
    if db.query(User).filter(User.mobile_number == mobile_number).first():
        raise ValueError("Mobile number already registered")
    user = User(email=email.lower().strip(), mobile_number=mobile_number.strip(), hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_access_token(email):
    expire = datetime.now() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRY))
    data = {"sub": email,"exp": expire}
    encoded_jwt = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def validate_user(detail:UserLogin, db: Session):
    user = db.query(User).filter(User.email == detail.email).first()
    if user and verify_password(detail.password,user.hashed_password):
        return {"token":create_access_token(user.email)}
    else:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")



