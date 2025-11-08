from fastapi import APIRouter, Request, Depends, HTTPException
from app.application.services.auth_service import AuthService
from backend.app.presentation.api.v1.shemas.account_shema import (
    UserRegister,
    UserResponse,
    LoginRequest,
)
from app.presentation.dependencies.service_factories import get_auth_service
from infrastructure.tasks.notifications.send_email import send_verification_email
from application.dtos.user_dto import UserDTO

router = APIRouter()


@router.post("/register", status_code=201)
async def register(
    request: Request,
    user_data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        base_url = str(request.base_url)
        user_dto: UserDTO = await auth_service.register_user(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            send_email_func=send_verification_email.delay,
            base_url=base_url,
        )
        return UserResponse(**user_dto.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/verify-email/{uidb64}/{token}")
async def verify_email(
    uidb64: str,
    token: str,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user_dto: UserDTO = await auth_service.verify_email(uidb64=uidb64, token=token)
        return UserResponse(**user_dto.to_dict())
    except (TypeError, ValueError, OverflowError, UnicodeDecodeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        tokens: dict[str, str] = await auth_service.login(
            login=login_data.login, password=login_data.password
        )
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
