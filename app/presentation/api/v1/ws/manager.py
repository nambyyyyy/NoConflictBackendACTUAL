from typing import Dict, List, Tuple
from fastapi import WebSocket, WebSocketDisconnect
from uuid import UUID


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[Tuple[UUID, WebSocket]]] = {}

    async def connect(self, room_name: str, user_id: UUID, websocket: WebSocket):
        """
        Подключаем пользователя к комнате. Комната может содержать максимум 2 разных user_id.
        """
        await websocket.accept()

        room = self.active_connections.setdefault(room_name, [])

        for uid, ws in room:
            if uid == user_id and ws is websocket:
                return

        unique_users = {uid for uid, _ in room}
        if user_id not in unique_users and len(unique_users) >= 2:
            await websocket.close(code=1008) 
            raise WebSocketDisconnect

        room.append((user_id, websocket))

    def disconnect(self, room_name: str, websocket: WebSocket):
        """
        Удаляем соединение. Если в комнате больше нет соединений, удаляем комнату.
        """
        room = self.active_connections.get(room_name)
        if not room:
            return

        room = [(uid, ws) for uid, ws in room if ws is not websocket]
        if room:
            self.active_connections[room_name] = room
        else:
            self.active_connections.pop(room_name, None)

    async def send_to_user(self, room_name: str, user_id: UUID, data: dict):
        """
        Отправить сообщение всем соединениям данного user_id в комнате (если у него открыто несколько вкладок).
        """
        room = self.active_connections.get(room_name, [])
        for uid, ws in room:
            if uid == user_id:
                await ws.send_json(data)

    async def send_to_other_user(
        self,
        room_name: str,
        current_user_id: UUID,
        data: dict,
    ):
        """
        Отправить сообщение всем соединениям «второго» участника, отличного от current_user_id.
        """
        room = self.active_connections.get(room_name, [])
        for uid, ws in room:
            if uid != current_user_id:
                await ws.send_json(data)

    async def broadcast(self, room_name: str, data: dict):
        """
        Отправить сообщение всем соединениям в комнате (и себе, и второму участнику).
        """
        room = self.active_connections.get(room_name, [])
        for _, ws in room:
            await ws.send_json(data)


manager = ConnectionManager()
