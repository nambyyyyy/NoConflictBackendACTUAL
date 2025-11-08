from fastapi import APIRouter, Request, Depends, HTTPException
from app.application.services.conflict_service import ConflictService
from backend.app.presentation.api.v1.shemas.conflict_shema import CreateConflict, ConflictDetailResponse
from app.presentation.dependencies.service_factories import get_conflict_service
from infrastructure.tasks.notifications.send_email import send_verification_email
from application.dtos.conflict_dto import ConflictDetailDTO
from typing import Any

router = APIRouter()


@router.post("/conflicts", status_code=201)
async def create_conflict(
    request: Request,
    conflict_data: CreateConflict,
    conflict_service: ConflictService = Depends(get_conflict_service)
):
    try:
        conflict_dto: ConflictDetailDTO = await conflict_service.create_conflict(
                request.user.id,
                conflict_data.partner_id,
                conflict_data.title,
                items=[item.model_dump() for item in conflict_data.items],
            )
        return ConflictDetailResponse(**conflict_dto.to_dict())  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")





