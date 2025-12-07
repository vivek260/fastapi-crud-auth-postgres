from sqlalchemy.orm import Session
from app.database.models import User
from app.utils.hashing import hash_password

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

