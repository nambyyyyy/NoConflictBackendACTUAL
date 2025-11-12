from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserRegister(BaseModel):
    email: str
    username: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    email_confirmed: bool
    

class LoginRequest(BaseModel):
    login: str
    password: str
    

class TokenPayload(BaseModel):
    sub: str