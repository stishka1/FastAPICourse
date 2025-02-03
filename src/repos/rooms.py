from datetime import date

from sqlalchemy import select, func
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import selectinload, joinedload

from src.models.bookings import BookingsOrm
from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomsWithRelationships


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        """
        ------------=================SQL запрос=================-----------------
            with rooms_count as (
                SELECT room_id, count(*) as rooms_booked from bookings
                where date_from <= '2024-11-30' and date_to >= '2024-07-01'
                group by room_id
            )
            select rooms.id as room_id, rooms.quantity, quantity - coalesce(rooms_booked, 0) as rooms_left from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
            where quantity - coalesce(rooms_booked, 0) > 0 and room_id in (select id from rooms where hotel_id= 5)
        """
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.comforts)) # или можно использовать joinedload (джоины вместо селектов)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [RoomsWithRelationships.model_validate(model) for model in result.scalars().all()]
        # await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))


    async def get_one_filtered(self, id, hotel_id):
        query = (
            select(self.model)
            .options(selectinload(self.model.comforts)) # или можно использовать joinedload (джоины вместо селектов)
            .filter(RoomsOrm.id == id, HotelsOrm.id == hotel_id)
        )

        result = await self.session.execute(query)
        return [RoomsWithRelationships.model_validate(model) for model in result.scalars().all()]



















