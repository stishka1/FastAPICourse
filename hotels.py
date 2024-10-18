from fastapi import FastAPI, Body, APIRouter, Query
from pydantic import BaseModel

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

hotels = [
    {
        "id": 1,
        "name": "Resort&SPA",
        "title": "Turkish"
    },
    {
        "id": 2,
        "name": "Miami Beach",
        "title": "Indonesia"
    },
    {
        "id": 3,
        "name": "EcoLine Resort",
        "title": "Gvinea Hotel"
    }
]

class Hotel(BaseModel):
    title: str
    name: str


@router.get("", summary="Получение списка всех отелей")
def main():
    global hotels

    return hotels

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
def update_one(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):

    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"]== hotel_id][0]


    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name

    return {"status": "200"}