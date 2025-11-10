from app.domain.interfaces.token_interface import EmailTokenRepository, JWTRepository
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
from typing import Optional


class FastAPIEmailTokenRepository(EmailTokenRepository):
    def __init__(self, secret_key: Optional[str], salt: str = "email-confirm"):
        if secret_key is None:
            raise
        self.serializer = URLSafeTimedSerializer(secret_key, salt)

    def generate_token(self, user_id: str) -> str:
        return self.serializer.dumps(user_id)

    def verify_token(self, token: str, max_age: int = 3600) -> Optional[str]:
        try:
            return self.serializer.loads(token, max_age)
        except (SignatureExpired, BadSignature):
            return None


class FastAPIJWTRepository(JWTRepository):
    def __init__(
        self,
        secret_key: Optional[str],
        algorithm: str = "HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 10000,
    ):
        if secret_key is None:
            raise
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict) -> str:
        """
        Создаёт JWT с payload (sub, role, id, exp).
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire, "token_type": "refresh", "jti": str(uuid4())})
        return jwt.encode(to_encode, self.secret_key, self.algorithm)
