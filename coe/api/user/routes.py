from fastapi import Request, Response, APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from coe.db.session import get_db
from coe.schemas.user import CreateUser, UserLogin, UpdateUser, UserRegisterResponse, ErrorResponse, UserLoginResponse, UserUpdateResponse, UserDeleteResponse, RefreshToken, RefreshTokenResponse, UserLogoutResponse, LoggedInUserResponse
from coe.services.user_service import create_user, login_user, remove_user, update_user
from coe.services.auth_service import create_access_token, get_current_user
from coe.models.user import User
from jose import JWTError, jwt
from config import settings

router = APIRouter(tags=["User"], prefix="/user")

@router.post(
    "/token/refresh", 
    response_model=RefreshTokenResponse
)
def refresh_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")

        new_access_token = create_access_token({"user_id": payload["user_id"]})
        
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="None",
            secure=True,
            path="/",
            max_age=settings.access_token_expire_minutes
        )

        result = {"message": "Access token refreshed successfully", "access_token": new_access_token}
        return RefreshTokenResponse.model_validate(result)
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

@router.post(
    "/register",
    response_model=UserRegisterResponse,
    responses={400: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
    openapi_extra={"is_public": True}
)
def register(user: CreateUser, db: Session = Depends(get_db)):
    new_user = create_user(user, db)
    result = {"message": "User registered successfully", "user_id": new_user.id}
    
    return UserRegisterResponse.model_validate(result)

@router.get(
    "/me",
    summary="Get current logged-in user info",
    response_model=LoggedInUserResponse
)
def get_me(current_user: User = Depends(get_current_user)):
    return LoggedInUserResponse.model_validate(current_user)

@router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={401: {"model": ErrorResponse}},
    openapi_extra={"is_public": True}
)
def login(response: Response, user: UserLogin, db: Session = Depends(get_db)):
    token_data = login_user(user, db)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    response.set_cookie(
        key="access_token",
        value=token_data["access_token"],
        httponly=True,
        secure=True,
        samesite="None",
        max_age=settings.access_token_expire_minutes,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=token_data["refresh_token"],
        httponly=True,
        secure=True,
        samesite="None",
        max_age=settings.refresh_token_expire_minutes,
        path="/user/token/refresh",
    )
    
    result = {"message": "User authenticated successfully", **token_data}
    return UserLoginResponse.model_validate(result)

@router.post(
    "/logout",
    response_model=UserLogoutResponse,
    summary="Logout user by clearing auth cookies",
    status_code=status.HTTP_200_OK
)
def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=True,
        samesite="None"
    )

    response.delete_cookie(
        key="refresh_token",
        path="/user/token/refresh",
        httponly=True,
        secure=True,
        samesite="None"
    )
    result = {"message": "Logged out successfully"}
    return UserLogoutResponse.model_validate(result)

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
        result = {"message": "User data updated successfully"}
        return UserUpdateResponse.model_validate(result)
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
        result = {"message": "User removed successfully"}
        return UserDeleteResponse.model_validate(result)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )