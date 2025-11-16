from password_validator import PasswordValidator
from domain.interfaces.password_interface import (
    PasswordValidator as IPasswordValidator,
)


class FastAPIPasswordValidator(IPasswordValidator):
    def __init__(self):
        self.schema = PasswordValidator()
        self.schema.min(8).max(
            64
        ).has().uppercase().has().lowercase().has().digits().has().symbols()

    def validate(self, plain_password: str) -> None:
        if not self.schema.validate(plain_password):
            raise ValueError("Слабый пароль: не выполнены требования безопасности.")
