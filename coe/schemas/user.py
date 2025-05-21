from pydantic import BaseModel, EmailStr, Field, constr, conint
from typing import Optional

NameStr = constr(strip_whitespace=True, min_length=1, max_length=50)
PasswordStr = constr(min_length=8, max_length=128)
UserID = conint(gt=0)

### Request Schemas
class CreateUser(BaseModel):
    first_name: NameStr = Field(..., description="First name of the user")
    last_name: NameStr = Field(..., description="Last name of the user")
    email: EmailStr = Field(..., description="User's email address")
    password: PasswordStr = Field(..., description="User's password (8–128 chars)")


class UpdateUser(BaseModel):
    id: UserID = Field(..., description="ID of the user to update")
    first_name: Optional[NameStr] = Field(None, description="Updated first name")
    last_name: Optional[NameStr] = Field(None, description="Updated last name")
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    password: Optional[PasswordStr] = Field(None, description="Updated password")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email for login")
    password: PasswordStr = Field(..., description="User's password")


class RemoveUser(BaseModel):
    id: UserID = Field(..., description="ID of the user to remove")


### Response Schemas
class UserRegisterResponse(BaseModel):
    message: str
    user_id: int

class UserLoginResponse(BaseModel):
    message: str

class UserUpdateResponse(BaseModel):
    message: str

class UserDeleteResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str