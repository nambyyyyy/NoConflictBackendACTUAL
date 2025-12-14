import json
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from domain.entities.user import User
from presentation.api.v1.ws.manager import manager
from application.services.conflict_service import ConflictService
from domain.entities.conflict import ConflictError, Conflict, ConflictItem
from domain.entities.conflict_event import EventType
from presentation.api.v1.dependencies import get_conflict_service, get_current_user_from_ws
from domain.dtos.conflict_dto import ConflictDetailDTO, ConflictItemDTO

router = APIRouter()



@router.websocket("/{slug}")
async def conflict_ws(
    websocket: WebSocket,
    slug: str,
    conflict_service: ConflictService = Depends(get_conflict_service),
    user: User = Depends(get_current_user_from_ws),
):
    room_name = f"conflict_{slug}"

    try:
        await conflict_service.get_conflict(user.id, slug)
    except ConflictError:
        await websocket.close(code=1008)
        return

    try:
        await manager.connect(room_name, user.id, websocket)
    except WebSocketDisconnect:
        return

    try:
        while True:
            raw = await websocket.receive_text()

            try:
                data: dict[str, Any] = json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                await websocket.send_json({"error": "Invalid JSON"})
                continue

            event_type = data.pop("event_type", None)
            if event_type != "update_item":
                await websocket.send_json(
                    {"error": "Допустимо только event_type = 'update_item'"}
                )
                continue

            item_id = data.pop("item_id", None)
            item_title = data.pop("item_title", None)
            new_value = data.pop("new_value", None)

            try:
                entity: Conflict | ConflictItem  = await conflict_service.update_item(
                    event_type=EventType.ITEM_UPDATE,
                    user_id=user.id,
                    slug=slug,
                    item_id=item_id,
                    item_title=item_title,
                    new_value=new_value
                )
                conflict_data, item_data = None, None
                
                if isinstance(entity, Conflict):
                    conflict_data = ConflictDetailDTO.create_dto(entity).to_dict()
                else:
                    item_data = ConflictItemDTO.create_dto(entity).to_dict()

                await manager.broadcast(room_name, {
                    "type": "item_updated",
                    "data": item_data if item_data else conflict_data,
                })

            except ConflictError as e:
                await websocket.send_json({"error": str(e)})
            except Exception as e:
                await websocket.send_json({"error": f"Internal error: {e}"})

    except WebSocketDisconnect:
        manager.disconnect(room_name, websocket)