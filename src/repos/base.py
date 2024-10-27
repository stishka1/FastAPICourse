from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.schemas.hotels import Hotel


class BaseRepository: # паттерн Репозиторий в действии (базовые CRUD операции для всего проекта)
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
            query = select(self.model)
            result = await self.session.execute(query)
            return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
            """
            паттерн DataMapper в действии -> возвращаем не объект базы данных, а pydantic схему
            с помощью from_attributes мы забираем данные с модели (все поля)
            """

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_stm = insert(self.model).values(**data.model_dump()).returning(self.model) # после вставки или любого изменения можно возвращать объект модели (1 строку), либо только 1 поле и т.д.
        #print(add_data_stm.compile(engine, compile_kwargs={"literal_binds": True})) # лог SQL транзакции в консоль с реальными данными - для дебага SQL запроса
        result = await self.session.execute(add_data_stm)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def update(self, data: BaseModel, **filter_by) -> None:
        upd_data_stm = update(self.model).filter_by(**filter_by).values(**data.model_dump()) # сначала фильтруемся, потом обновляем и так всегда
        await self.session.execute(upd_data_stm)

    async def update_partially(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        upd_data_stm = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))  # сначала фильтруемся, потом обновляем и так всегда
        await self.session.execute(upd_data_stm)

    async def delete(self, **filter_by) -> None:
        delete_data_stm = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stm)