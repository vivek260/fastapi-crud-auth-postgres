from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse,UserLogin
from app.services.user_service import create_user,create_access_token,validate_user
from app.database.connection import get_db

router = APIRouter()

@router.post("/signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(str(payload.email),payload.mobile_number,payload.password,db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(payload:UserLogin, db: Session = Depends(get_db)):
    print("Login received")
    print("Payload:", payload)
    try:
        return validate_user(payload,db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

