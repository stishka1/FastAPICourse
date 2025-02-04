from datetime import date

from sqlalchemy import select, func
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import HotelDataMapper
from src.repos.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    # сначала получаем все свободные номера, потом по этим свободным номерам вытаскиваем отели
    async def get_filtered_by_time(self,
                                   date_from: date,
                                   date_to: date,
                                   location,
                                   title,
                                   limit,
                                   offset,
                                   ) -> list[Hotel]: # возвращается pydantic схема Hotel

        # получаем id комнат на определенные даты
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from,
                                                 date_to=date_to)

        # получаем все id отелей
        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        # по id отелей получаем всю информацию о них
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids)) # получив id отелей мы фильтруемся по ним и затем уже фильтруемся по location/title (опциональные)

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

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]




















