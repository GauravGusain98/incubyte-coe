from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from coe.schemas.user import CreateUser, UserLogin, RemoveUser, UpdateUser
from coe.db.session import SessionLocal
from coe.services.user_service import create_user, login_user, remove_user, update_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: CreateUser, db: Session = Depends(get_db)):
    new_user = create_user(user, db)
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user = login_user(user, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return {"message": "User authenticated successfully"}

@router.put("/update-user", summary="Update user data by ID")
def delete_user(user: UpdateUser, db: Session = Depends(get_db)):
    success = update_user(user, db)
    if success:
        return {"message": "User data updated successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@router.delete("/remove-user", summary="Remove a user by ID")
def delete_user(user: RemoveUser, db: Session = Depends(get_db)):
    success = remove_user(user, db)
    if success:
        return {"message": "User removed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )