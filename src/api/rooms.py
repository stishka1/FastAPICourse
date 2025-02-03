from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repos.rooms import RoomsRepository
from src.schemas.comfort import RoomsComfortAdd
from src.schemas.rooms import AddRoom, RoomsPatch, AddRoomRequest, RoomsPatchRequest

router = APIRouter(prefix="/hotels", tags=['Номера'])

@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_all_rooms(db: DBDep, hotel_id: int, date_from: date = Query(example="2024-07-01"), date_to: date = Query(example='2024-07-31')):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)



@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить информацию об 1 номере")
async def get_one_room(db: DBDep, room_id: int, hotel_id: int): # указали hotel_id иначе не будет проверки по отелю и у любых отелей будет какой-то номер
    return await db.rooms.get_one_filtered(id=room_id, hotel_id=hotel_id)



@router.post("/{hotel_id}/rooms", summary="Добавить новый номер")
async def add_new_room(db: DBDep, hotel_id: int, room_data: AddRoomRequest = Body()): # другая схема чтобы hotel_id брать из параметров пути
    _room_data = AddRoom(hotel_id=hotel_id, **room_data.model_dump()) # объединяем hotel_id и pydantic схему в 1 схему!
    room = await db.rooms.add(_room_data)


    # добавление удобств к комнате
    # в такой вид: [
    #                  RoomsComfortAdd(room_id=10, comfort_id=1),
    #                  RoomsComfortAdd(room_id=10, comfort_id=2)
    #               ]
    rooms_comfort_data = [RoomsComfortAdd(room_id=room.id, comfort_id=com_id) for com_id in room_data.comfort_ids]
    await db.rooms_comfort.add_bulk(rooms_comfort_data)

    await db.commit()
    return {"status": "200", "data": room}





@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить все данные о номере")
async def update_room(db: DBDep, room_data: AddRoomRequest, room_id: int | None, hotel_id: int | None):
    _room_data = AddRoom(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)

    # Работа с m2m таблицей удобств добавление / удаление
    await db.rooms_comfort.set_room_comfort(room_id, comfort_ids=room_data.comfort_ids)


# мой вариант решения
#    room_comfort_data = await db.rooms_comfort.get_filtered(room_id=room_id) # [RoomsComfort(room_id=11, comfort_id=1, id=1), RoomsComfort(room_id=11, comfort_id=2, id=2)]
#    d = {room_id: [k.comfort_id for k in room_comfort_data]} # {11: [2, 1]}
#
#    # добавить то, чего нет. Что есть в боди и БД - не трогаем.
#    for i in room_data.comfort_ids:
#           if i not in d[room_id]:
#               await db.rooms_comfort.add(RoomsComfortAdd(room_id=room_id, comfort_id=i))
#    # удалить то, чего нет
#    for j in d[room_id]:
#        if j not in room_data.comfort_ids:
#            await db.rooms_comfort.delete(room_id=room_id, comfort_id=j)

    await db.commit()
    return {"status": "200"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных номера")
async def update_partially(db: DBDep,
                           room_id: int,
                           hotel_id: int,
                           room_data: RoomsPatchRequest
                           ):

    _room_data_dict = room_data.model_dump(exclude_unset=True) # проверка через pydantic словарик наличия comfort_ids
    _room_data = RoomsPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.update_partially(_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)

    # проверка на присутствие чтобы патч корректно выполнился
    if "comfort_ids" in _room_data_dict:
        await db.rooms_comfort.set_room_comfort(room_id, comfort_ids=_room_data_dict["comfort_ids"])

    await db.commit()
    return {"status": "200"}






@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер по id")
async def delete_room(db: DBDep, room_id: int, hotel_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}