from datetime import date

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.dependencies import PaginationDep, DBDep
from fastapi import APIRouter, Query, Body
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from sqlalchemy import insert, select, func # func - можем пользоваться функциями SQL в sqlalchemy

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

@router.get("/{hotel_id}", summary="Получить информацию об отеле")
async def get_one_hotel(db: DBDep, hotel_id: int):
    """
        <h1>Получаем 1 отель по его номеру</h1>
    """
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.get("", summary="Получение списка всех отелей")
async def get_all(pagination: PaginationDep, # для переиспользования пагинации
                db: DBDep,
                title: str | None = Query(None, description="Название отеля"),
                location: str | None = Query(None, description="Адрес отеля"),
                date_from: date = Query(example="2024-08-01", description="Дата заселения"),
                date_to: date = Query(example='2024-08-10', description="Дата выезда")
               ):
    """
        <h1>По умолчанию 5 отелей</h1>
    """
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1)
    # )

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
    )
@router.post("", summary="Добавление нового отеля")
async def add_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    "3": {
        "summary": "Египет",
        "value": {
            "title": "Domina Coral Bay Resort, Diving, SPA & Casino 5*",
            "location": "мухафаза Южный Синай, Шарм-эль-Шейх, Domina Coral Bay"

        }
    },
    "4": {
        "summary": "Египет",
        "value": {
            "title": "Жасмин Палас Резорт и СПА 5*",
            "location": "мухафаза Красное Море, Дорога Сахл Хашиш"

        }
    },
    "5": {
        "summary": "Тайланд",
        "value": {
            "title": "Long Beach Garden Hotel & Pavilions",
            "location": "Nakluea 16 soi, 499/7, г. Паттайя"

        }
    },
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
        #await session.commit() # коммит здесь, а не в BaseRepository т.к. может быть много вставок/изменений данных и мы должны находиться в рамках 1 транзакции!
    return {"status": "200", "data": hotel}





@router.put("", summary="Обновление всех данных об отеле")
async def update(db: DBDep, hotel_data: HotelAdd, hotel_id: int | None): # вынесли отдельно id (не брали из схемы) чтобы параметр появился в пути и можно было вводить и обновлять по нему
    await db.hotels.update(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "200"}




@router.patch("", summary="Частичное обновление данных отеля")
async def update_partially(db: DBDep, hotel_data: HotelPatch, hotel_id: int): # вынесли отдельно id (не брали из схемы) чтобы параметр появился в пути и можно было вводить и обновлять по нему
    """
        <h1>Частичное обновление данных об отеле</h1>
    """
    await db.hotels.update_partially(hotel_data, exclude_unset=True, id=hotel_id) # все благодаря незаданным параметрам exclude_unset
    await db.commit()
    return {"status": "200"}




@router.delete("/{hotel_id}", summary="Удаление отеля по id")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "200"}