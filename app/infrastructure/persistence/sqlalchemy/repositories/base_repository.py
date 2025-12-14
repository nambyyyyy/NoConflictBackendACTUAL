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

    def dict_for_entity(
        self, orm_object, include_relations: bool = True
    ) -> Optional[dict]:
        try:
            state = inspect(orm_object)
            mapper = state.mapper
            result = {}

            # 1️⃣ Только колонки
            for column in mapper.column_attrs:
                result[column.key] = getattr(orm_object, column.key)

            # 2️⃣ Relationships - только если нужно И только для uselist (коллекции)
            if include_relations:
                for name, relation in mapper.relationships.items():
                    # Пропускаем обратные ссылки (не uselist = single object pointing back)
                    if not relation.uselist:
                        continue

                    value = getattr(orm_object, name)
                    if value is not None:
                        # Для вложенных - НЕ включаем их relationships
                        result[name] = [
                            self.dict_for_entity(v, include_relations=False)
                            for v in value
                        ]

            return result
        except Exception as e:
            print("Ошибка в dict_for_entity:", e)
