from sqlalchemy import select, func
from sqlalchemy.dialects.mysql import insert

from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower())) # в sqlalchemy по умолчанию встроена защита от sql иньекций, но с помощью contains мы страхуемся в случае с psycopg...
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, **data):
        # existing_hotel = self.get_one_or_none(title=title)
        # if not existing_hotel:
            query = insert(self.model).values(**data)
            await self.session.execute(query)