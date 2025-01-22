from datetime import date

from sqlalchemy import select, func
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.repos.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset) -> list[Hotel]: # возвращается pydantic схема Hotel
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
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    # сначала получаем все свободные номера, потом по этим свободным номерам вытаскиваем отели
    async def get_filtered_by_time(self, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids))



















