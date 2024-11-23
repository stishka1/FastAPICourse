from fastapi import APIRouter, Query, Body
from watchfiles import awatch

from src.database import async_session_maker
from src.repos.base import BaseRepository
from src.repos.hotels import HotelsRepository
from src.repos.rooms import RoomsRepository
from src.schemas.rooms import AddRoom, RoomsPatch

router = APIRouter(prefix="/hotels", tags=['Номера'])

@router.get("", summary="Получить все номера")
async def get_all_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()

@router.get("/{room_id}", summary="Получить информацию о номере")
async def get_one_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)

@router.post("", summary="Добавить новый номер")
async def add_new_room(room_data: AddRoom = Body()):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "200", "data": room}

@router.put("", summary="Обновить все данные о номере")
async def update_room(room_data: AddRoom, room_id: int | None):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, id=room_id)
        await session.commit()
    return {"status": "200"}

@router.patch("", summary="Частичное обновление данных номера")
async def update_partially(room_data: RoomsPatch, room_id: int | None):
    async with async_session_maker() as session:
        await RoomsRepository(session).update_partially(room_data, id=room_id, exclude_unset=True)
        await session.commit()
    return {"status": "200"}

@router.delete("/{room_id}", summary="Удалить номер по id")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "ok"}