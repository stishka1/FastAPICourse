from datetime import date

from sqlalchemy import select, func
from sqlalchemy.sql.functions import coalesce

from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


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
        rooms_count = (
            select(BookingsOrm.room_id, func.count(BookingsOrm.room_id).label('rooms_booked'))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from <= date_from, BookingsOrm.date_to >= date_to)
            .group_by(BookingsOrm.room_id)
            .cte(name='rooms_count')
        )

        """
        !select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left from rooms
        """
        rooms_left_table = (
            select(
            RoomsOrm.id.label('room_id'),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('rooms_left'), # из CTE достаются столбцы через атрибут c
        )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name='rooms_left_table')
        )

        rooms_ids_for_hotel = (
            select(RoomsOrm.id).select_from(RoomsOrm)
            .filter_by(hotel_id = hotel_id)
            .subquery(name="rooms_ids_for_hotel") # для алхимии что это подзапрос, не Common Table Expression (CTE)
        )

        query = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel)
                )
        )

        return await self.get_filtered(RoomsOrm.id.in_(query))