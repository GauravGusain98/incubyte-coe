from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from coe.schemas.user import UserCreate
from coe.db.session import SessionLocal
from coe.services.user_service import create_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(user, db)
    return {"message": "User registered successfully", "user_id": new_user.id}