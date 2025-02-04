from typing import TypeVar
from pydantic import BaseModel
from src.database import Base

# для подсказов при наведении мышкой (всплывающие подсказки)
DBModelType = TypeVar('DBModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    # у паттерна DataMapper 2 метода
    # превращаем SQLAlchemy модель в pydantic схему
    # модель не привязана к схеме, а схема к модели

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    # принимаем данные pydantic схемы и возвращаем модель алхимии
    def map_to_persistense_entity(cls, data):
        return cls.db_model(**data.model_dump())