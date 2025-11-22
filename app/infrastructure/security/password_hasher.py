from passlib.context import CryptContext
from domain.interfaces.password_interface import PasswordHasher


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,   # 64 MB вместо ~512 MB
    argon2__time_cost=2,         # 2 итерации — быстро, но безопасно
    argon2__parallelism=2
)

class FastAPIPasswordHasher(PasswordHasher):
    # MAX_BCRYPT_BYTES = 72 

    # def _prepare_password(self, plain_password: str) -> str:
    #     # Убедимся, что не превышаем предел bcrypt
    #     password_bytes = plain_password.encode('utf-8')
    #     if len(password_bytes) > self.MAX_BCRYPT_BYTES:
    #         password_bytes = password_bytes[:self.MAX_BCRYPT_BYTES]
    #         # декодируем обратно в строку, отбрасывая некорректные байты аккуратно
    #         plain_password = password_bytes.decode('utf-8', errors='ignore')
    #     return plain_password
    
    def hash(self, plain_password: str) -> str:
        """Возвращает хеш пароля (обрезает при необходимости)."""
        # plain_password = self._prepare_password(plain_password)
        return pwd_context.hash(plain_password)
 

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет, совпадает ли пароль с хешем."""
        # plain_password = self._prepare_password(plain_password)
        return pwd_context.verify(plain_password, hashed_password)