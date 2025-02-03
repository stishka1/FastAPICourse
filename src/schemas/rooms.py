from pydantic import BaseModel, ConfigDict

from src.schemas.comfort import Comfort


# нет hotel_id специально чтобы забирать из параметров пути для POST
class AddRoomRequest(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    comfort_ids: list[int] = [] # если ничего не передаем - то пустой массив лучше передавать

class AddRoom(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int

class Room(AddRoom):
    id : int

    # Когда из репозитория возвращаем данные легко превращаем ответ алхимии к pydantic схеме
    # Они не являются словарями. Это экземпляры класса алхимии.
    model_config = ConfigDict(from_attributes=True)

class RoomsPatchRequest(BaseModel):
        title: str | None = None
        description: str | None = None
        price: int | None = None
        quantity: int | None = None
        comfort_ids: list[int] = []

# у опционального поля | None всегда должно быть задано значение = None
class RoomsPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class RoomsWithRelationships(Room):
    comforts: list[Comfort]





















