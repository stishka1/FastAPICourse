from sqlalchemy import select, delete, insert

from src.models.comfort import ComfortOrm, RoomsComfortOrm
from src.repos.base import BaseRepository
from src.schemas.comfort import Comfort, RoomsComfort


class ComfortRepository(BaseRepository):
    model = ComfortOrm
    schema = Comfort


class RoomsComfortRepository(BaseRepository):
    model = RoomsComfortOrm
    schema = RoomsComfort

    async def set_room_comfort(self, room_id: int, comfort_ids: list[int]) -> None:
        query = (
            select(self.model.comfort_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(query)
        current_comfort_ids: list[int] = res.scalars().all()
        comfort_ids_to_delete: list[int] = list(set(current_comfort_ids) - set(comfort_ids)) # [4, 1, 2] - [2, 3] = [1, 4]
        comfort_ids_to_add: list[int] = list(set(comfort_ids) - set(current_comfort_ids)) # [2, 3] - [4, 1, 2] = [3]

        if comfort_ids_to_delete:
            delete_m2m_comfort_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.comfort_id.in_(comfort_ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_comfort_stmt)

        if comfort_ids_to_add:
            insert_m2m_comfort_stmt = (
                insert(self.model)
                # нам нужен список словариков
                .values([{"room_id": room_id, "comfort_id": com_id} for com_id in comfort_ids_to_add])
                )
            await self.session.execute(insert_m2m_comfort_stmt)









