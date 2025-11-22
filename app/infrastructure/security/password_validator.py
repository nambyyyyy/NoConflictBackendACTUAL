from password_validator import PasswordValidator
from domain.interfaces.password_interface import (
    PasswordValidator as IPasswordValidator,
)
import re


class FastAPIPasswordValidator(IPasswordValidator):
    
    def validate(self, password: str) -> bool:
        # Проверяем длину
        if len(password) < 6:
            return False
        # Проверяем наличие хотя бы одной буквы и хотя бы одной цифры
        if not re.search(r'[A-Za-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
