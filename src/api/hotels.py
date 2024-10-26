from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.dependencies import PaginationDep
from fastapi import APIRouter, Query, Body

from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPatch

from sqlalchemy import insert, select, func # func - можем пользоваться функциями SQL в sqlalchemy

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

@router.get("", summary="Получение списка всех отелей")
async def main(pagination: PaginationDep, # для переиспользования пагинации
               title: str | None = Query(None, description="Название отеля"),
               location: str | None = Query(None, description="Адрес отеля"),
               ):
    """
        <h1>По умолчанию 5 отелей</h1>
    """
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower())) # в sqlalchemy по умолчанию встроена защита от sql иньекций, но с помощью contains мы страхуемся в случае с psycopg...
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower()))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

@router.post("", summary="Добавление нового отеля")
async def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Анапа",
        "value": {
            "title": "Mantera Resort & Congress 5*",
            "location": "посёлок городского типа Сириус, Голубая улица, 1А"

        }
    },
    "2": {
        "summary": "Турция",
        "value": {
            "title": "Windsor Hotel & Convention Center Istanbul 5*",
            "location": "Стамбул, Байрампаша, махалле Енидоган, улица Эрджиес, 7"

        }
    },
})):
    async with async_session_maker() as session:
        add_stat =  insert(HotelsOrm).values(**hotel_data.model_dump()) # раскрытие в кварги, pydantic схема в словарь, потом раскрытие словаря
        #print(add_stat.compile(engine, compile_kwargs={"literal_binds": True})) # лог SQL транзакции в консоль с реальными данными - для дебага SQL запроса
        await session.execute(add_stat)
        await session.commit()
    return {"status": "200"}

@router.put("/{hotel_id}", summary="Обновление всех данных об отеле")
def update_all(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"]== hotel_id][0]
    hotel["name"] = hotel_data.name
    hotel["title"] = hotel_data.title

    return hotels

@router.delete("/{hotel_id}", summary="Удаление отеля по id")
def delete_hotel(hotel_id: int):
    global hotels
    for i in hotels:
        if hotel_id == i['id']:
            hotels.remove(i)
    return {"status": "200"}



@router.patch("/{hotel_id}", summary="Частичное обновление данных отеля")
def update_one(hotel_id: int, hotel_data: HotelPatch):
    """
        <h3>Частичное обновление данных об отеле</h3>
    """

    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"]== hotel_id][0]


    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name

    return {"status": "200"}