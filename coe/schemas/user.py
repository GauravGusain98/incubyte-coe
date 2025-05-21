from pydantic import BaseModel

### Request Schemas
class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UpdateUser(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

class RemoveUser(BaseModel):
    id: int


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