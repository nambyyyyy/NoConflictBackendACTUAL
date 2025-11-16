from dataclasses import dataclass, fields
from uuid import UUID
from datetime import datetime

@dataclass
class BaseDTO:
    def to_dict(self) -> dict:
        """Сериализация DTO в dict (UUID → str, datetime → isoformat)."""
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, UUID):
                result[f.name] = str(value)
            elif isinstance(value, datetime):
                result[f.name] = value.isoformat()
            elif isinstance(value, list):
                result[f.name] = [
                    v.to_dict() if hasattr(v, "to_dict") else v for v in value
                ]
            else:
                result[f.name] = value
        return result

    @classmethod
    def create_dto(cls, entity: object):
        """Создает DTO из любой сущности с совпадающими именами полей."""
        dto_fields = {f.name for f in fields(cls)}
        data = {
            name: getattr(entity, name) for name in dto_fields if hasattr(entity, name)
        }
        return cls(**data)
