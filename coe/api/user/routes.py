from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from coe.schemas.user import CreateUser, UserLogin, UpdateUser, UserRegisterResponse, ErrorResponse, UserLoginResponse, UserUpdateResponse, UserDeleteResponse, RefreshToken
from coe.db.session import SessionLocal
from coe.services.user_service import create_user, login_user, remove_user, update_user
from coe.services.auth_service import get_current_user, create_access_token
from coe.models.user import User
from jose import JWTError, jwt
from config import settings

router = APIRouter(tags=["User"], prefix="/user")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token/refresh", summary="Get new access token using refresh token")
def refresh_access_token(token: RefreshToken = Body(...)):
    try:
        payload = jwt.decode(token.refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")
        
        new_access_token = create_access_token({"user_id": payload["user_id"]})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")

@router.post(
    "/register",
    response_model=UserRegisterResponse,
    responses={400: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED
)
def register(user: CreateUser, db: Session = Depends(get_db)):
    new_user = create_user(user, db)
    
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={401: {"model": ErrorResponse}}
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token_data = login_user(user, db)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {"message": "User authenticated successfully", **token_data}

@router.put(
    "/{user_id}",
    summary="Update user data by ID",
    response_model=UserUpdateResponse,
    responses={404: {"model": ErrorResponse}}
)
def update_user_details(
    user_id: int, 
    user_data: UpdateUser, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = update_user(user_id, user_data, db)
    if success:
        return {"message": "User data updated successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@router.delete(
    "/{user_id}",
    summary="Remove a user by ID",
    response_model=UserDeleteResponse,
    responses={404: {"model": ErrorResponse}}
)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    success = remove_user(user_id, db)
    if success:
        return {"message": "User removed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )