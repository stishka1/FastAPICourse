from src.api.dependencies import PaginationDep
from fastapi import FastAPI, APIRouter, Query
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("", summary="Получение списка всех отелей")
def main(pagination: PaginationDep, # для переиспользования пагинации
         id: str | None = Query(None, description="Номер отеля")):
    """
        <h1>По умолчанию 5 отелей</h1>
    """
    global hotels

    # пагинация
    if pagination.page and pagination.per_page:
        start = (pagination.page - 1) * pagination.per_page
        end = pagination.page * pagination.per_page
        paginated = hotels[start:end]

    else:
        paginated = hotels[:5]

    return paginated

@router.post("/{hotel_id}", summary="Добавление нового отеля")
def add_hotel(hotel_id: int | None, hotel_data: Hotel):
    global hotels
    if hotel_id not in hotels:
        hotels.append(
                {
                    "id": hotel_id,
                    "name": hotel_data.name,
                    "title": hotel_data.title,
                }
            )
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