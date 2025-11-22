from sqlalchemy import inspect
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
from domain.entities.protocols import T
from dataclasses import fields

class SQLAlchemyBaseRepository:
    
    def __init__(self, db_session: AsyncSession, entity: Type[T]):
        self.db_session = db_session
        self.entity = entity
    
    def create_from_data(self, data: dict) -> T:
        allowed_keys = {f.name for f in fields(self.entity)}
        filtered = {k: v for k, v in data.items() if k in allowed_keys}

            
        return self.entity.create_entity(**filtered)
        

    def fast_dict_for_entity(self, orm_object) -> dict:
        data = {
            column.key: getattr(orm_object, column.key)
            for column in inspect(orm_object).mapper.column_attrs
        }
        return data
    
    def dict_for_entity(self, orm_object, seen: Optional[set[int]] = None) -> dict:
        try:
            if seen is None:
                seen = set()

            obj_id = id(orm_object)
            if obj_id in seen:  # чтобы избежать рекурсии
                return {"_ref": str(obj_id)}

            seen.add(obj_id)

            state = inspect(orm_object)
            mapper = state.mapper  # ✅ получение маппера модели

            result = {}

            # 1️⃣ Простые колонки
            for column in mapper.column_attrs:
                result[column.key] = getattr(orm_object, column.key)

            # 2️⃣ Relationships
            for name, relation in mapper.relationships.items():
                value = getattr(orm_object, name)

                if value is None:
                    result[name] = None
                elif relation.uselist:
                    result[name] = [self.dict_for_entity(v, seen=seen) for v in value]
                else:
                    result[name] = self.dict_for_entity(value, seen=seen)
        except Exception as e:
            print("Ошибка в dict_for_entity:", e)

        return result



