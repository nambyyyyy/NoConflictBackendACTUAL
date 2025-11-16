from dataclasses import dataclass
from uuid import UUID
from domain.dtos.base_dto import BaseDTO


@dataclass
class UserDTO(BaseDTO):
    """DTO для передачи данных о пользователе"""

    id: UUID
    email: str
    username: str
    email_confirmed: bool

