from sqlalchemy import inspect
from typing import Optional

class UtilRepository:

    def fast_dict_for_entity(self, orm_object) -> dict:
        data = {
            column.key: getattr(orm_object, column.key)
            for column in inspect(orm_object).mapper.column_attrs
        }
        return data
    
    def dict_for_entity(self, orm_object, seen: Optional[set[int]] = None) -> dict:

        if seen is None:
            seen = set()

        obj_id = id(orm_object)
        if obj_id in seen:  # чтобы избежать вечной рекурсии
            return {"_ref": str(obj_id)}

        seen.add(obj_id)

        mapper = inspect(orm_object)
        result = {}

        # 1️⃣ Простые колонки (column_attrs)
        for column in mapper.column_attrs:
            result[column.key] = getattr(orm_object, column.key)

        # 2️⃣ Relationships
        for name, relation in mapper.relationships.items():
            value = getattr(orm_object, name)

            if value is None:
                result[name] = None
            elif relation.uselist:
                # Список зависимых объектов
                result[name] = [self.dict_for_entity(v, seen=seen) for v in value]
            else:
                # Один связанный объект
                result[name] = self.dict_for_entity(value, seen=seen)

        return result



