from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
import re


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, password2, values):
        if "password" in values and password2 != values["password"]:
            raise ValueError("Пароли не совпадают")
        return password2

    @field_validator("username")
    def validate_username(cls, username):
        username = username.strip()
        if len(username) < 3:
            raise ValueError("Логин должен быть не менее 3 символов")
        if not re.match(r"^[a-zA-Z0-9._-]+$", username):
            raise ValueError("Только буквы, цифры, точка, дефис и подчёркивание")
        if re.match(r"^\d+$", username):
            raise ValueError("Нельзя использовать только цифры в имени")
        return username
    


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
