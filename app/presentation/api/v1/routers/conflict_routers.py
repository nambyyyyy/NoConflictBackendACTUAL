from fastapi import APIRouter, Request, Depends, HTTPException
from app.application.services.conflict_service import ConflictService
from app.application.services.user_service import UserService
from backend.app.presentation.api.v1.shemas.conflict_shema import (
    CreateConflict,
    ConflictDetailResponse,
)
from backend.app.presentation.api.v1.dependencies import (
    get_conflict_service,
    get_current_user,
)
from infrastructure.tasks.notifications.send_email import send_verification_email
from application.dtos.conflict_dto import ConflictDetailDTO
from application.dtos.user_dto import UserDTO
from typing import Optional, Any, Callable, Awaitable
from fastapi import status

router = APIRouter()

async def base_action()

@router.post("/conflicts", status_code=status.HTTP_201_CREATED)
async def create_conflict(
    conflict_data: CreateConflict,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    try:
        conflict_dto: ConflictDetailDTO = await conflict_service.create_conflict(
            current_user.id,
            conflict_data.partner_id,
            conflict_data.title,
            items=[item.model_dump() for item in conflict_data.items],
        )
        return ConflictDetailResponse(**conflict_dto.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/conflicts/{slug}",
    response_description="Get conflict",
    status_code=status.HTTP_200_OK,
)
async def get_conflict(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    try:
        conflict_dto: ConflictDetailDTO = await conflict_service.get_conflict(
            current_user.id, slug
        )
        return ConflictDetailResponse(**conflict_dto.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch(
    "/conflicts/{slug}/cancel",
    response_description="Cancel conflict",
    status_code=status.HTTP_200_OK,
)
async def cancel_conflict(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    try:
        conflict_dto: ConflictDetailDTO = await conflict_service.cancel_conflict(
            current_user.id, slug
        )
        return ConflictDetailResponse(**conflict_dto.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/conflicts/{slug}/delete",
    response_description="Delete conflict",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conflict(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    try:
        await conflict_service.delete_conflict(current_user.id, slug)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch(
    "/conflicts/{slug}/offer-truce",
    response_description="Create offer truce in conflict",
    status_code=status.HTTP_200_OK,
)
async def create_offer_truce(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    try:
        conflict_dto: ConflictDetailDTO = await conflict_service.create_offer_truce(
            current_user.id, slug
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch(
    "/conflicts/{slug}/offer-truce/cancel",
    response_description="Cancel offer truce in conflict",
    status_code=status.HTTP_200_OK,
)
async def cancel_offer_truce(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    try:
        conflict_dto: ConflictDetailDTO = await conflict_service.cancel_offer_truce(
            current_user.id, slug
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.patch(
    "/conflicts/{slug}/offer-truce/accept",
    response_description="Accept offer truce in conflict",
    status_code=status.HTTP_200_OK,
)
async def accept_offer_truce(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    try:
        conflict_dto: ConflictDetailDTO = await conflict_service.accepted_offer_truce(
            current_user.id, slug
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")