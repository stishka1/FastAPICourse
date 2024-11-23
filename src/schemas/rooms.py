from pydantic import BaseModel

class AddRoom(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int

class Room(AddRoom):
    id : int

class RoomsPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None