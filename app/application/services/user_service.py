from domain.interfaces.user_interface import UserRepository
from uuid import UUID
from typing import Optional
from domain.entities.user import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
    
    async def get_user(self, user_id: UUID) -> User:
        user: Optional[User] = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        
        return user
        
