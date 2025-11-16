from domain.interfaces.token_interface import EmailTokenRepository, JWTRepository
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
from typing import Optional
from domain.entities.user import User


class FastAPIEmailTokenRepository(EmailTokenRepository):
    def __init__(self, secret_key: Optional[str], salt: str = "email-confirm"):
        if secret_key is None:
            raise
        self.serializer = URLSafeTimedSerializer(secret_key, salt)

    def generate_token(self, user_id: str) -> str:
        return self.serializer.dumps(user_id)

    def verify_token(self, token: str, max_age: int = 3600) -> bool:
        try:
            self.serializer.loads(token, max_age)
            return True
        except (SignatureExpired, BadSignature):
            return False


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

    def create_access_token(self, user: User) -> str:
        payload = {
            "user_id": str(user.id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
            "token_type": "refresh",
            "jti": str(uuid4()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user: User) -> str:
        payload = {
            'user_id': str(user.id),
            'exp': datetime.now(timezone.utc) + timedelta(days=30),
            'token_type': 'refresh',
            'jti': str(uuid4())
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)


