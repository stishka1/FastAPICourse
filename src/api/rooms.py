from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repos.rooms import RoomsRepository
from src.schemas.rooms import AddRoom, RoomsPatch, AddRoomRequest, RoomsPatchRequest

router = APIRouter(prefix="/hotels", tags=['Номера'])

@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_all_rooms(db: DBDep, hotel_id: int, date_from: date = Query(example="2024-07-01"), date_to: date = Query(example='2024-07-31')):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить информацию о номере")
async def get_one_room(db: DBDep, room_id: int, hotel_id: int): # указали hotel_id иначе не будет проверки по отелю и у любых отелей будет какой-то номер
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/{hotel_id}/rooms", summary="Добавить новый номер")
async def add_new_room(db: DBDep, hotel_id: int, room_data: AddRoomRequest = Body()): # другая схема чтобы hotel_id брать из параметров пути
    _room_data = AddRoom(hotel_id=hotel_id, **room_data.model_dump()) # объединяем hotel_id и pydantic схему в 1 схему!
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "200", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить все данные о номере")
async def update_room(db: DBDep, room_data: AddRoomRequest, room_id: int | None, hotel_id: int | None):
    _room_data = AddRoom(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "200"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных номера")
async def update_partially(db: DBDep, room_data: RoomsPatchRequest, room_id: int, hotel_id: int):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update_partially(room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "200"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер по id")
async def delete_room(db: DBDep, room_id: int, hotel_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}