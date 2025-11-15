from fastapi import APIRouter, Depends, HTTPException
from app.application.services.conflict_service import ConflictService
from backend.app.presentation.api.v1.shemas.conflict_shema import (
    CreateConflict,
    ConflictDetailResponse,
)
from backend.app.presentation.api.v1.dependencies import (
    get_conflict_service,
    get_current_user,
)
from application.dtos.conflict_dto import ConflictDetailDTO
from application.dtos.user_dto import UserDTO
from fastapi import status
from functools import wraps

router = APIRouter()


def conflict_action(service_method_name: str, response_model_cls=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            conflict_service = kwargs.get("conflict_service")
            slug = kwargs.get("slug")
            try:
                method = getattr(conflict_service, service_method_name)
                result = await method(current_user.id, slug)
                if response_model_cls and result:
                    return response_model_cls(**result.to_dict())
                return None
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail="Internal server error"
                ) from e

        return wrapper

    return decorator


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
@conflict_action("get_conflict", ConflictDetailResponse)
async def get_conflict(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    pass


@router.patch(
    "/conflicts/{slug}/cancel",
    response_description="Cancel conflict",
    status_code=200,
)
@conflict_action("cancel_conflict", ConflictDetailResponse)
async def cancel_conflict(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    pass


@router.delete(
    "/conflicts/{slug}/delete",
    response_description="Delete conflict",
    status_code=status.HTTP_204_NO_CONTENT,
)
@conflict_action("delete_conflict", ConflictDetailResponse)
async def delete_conflict(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    pass


@router.patch(
    "/conflicts/{slug}/offer-truce",
    response_description="Create offer truce in conflict",
    status_code=status.HTTP_200_OK,
)
@conflict_action("create_offer_truce", ConflictDetailResponse)
async def create_offer_truce(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    pass


@router.patch(
    "/conflicts/{slug}/offer-truce/cancel",
    response_description="Cancel offer truce in conflict",
    status_code=status.HTTP_200_OK,
)
@conflict_action("cancel_offer_truce", ConflictDetailResponse)
async def cancel_offer_truce(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    pass


@router.patch(
    "/conflicts/{slug}/offer-truce/accept",
    response_description="Accept offer truce in conflict",
    status_code=status.HTTP_200_OK,
)
@conflict_action("accepted_offer_truce", ConflictDetailResponse)
async def accept_offer_truce(
    slug: str,
    current_user: UserDTO = Depends(get_current_user),
    conflict_service: ConflictService = Depends(get_conflict_service),
):
    pass
