from pydantic import BaseModel, ConfigDict


class ComfortAdd(BaseModel):
    title: str

class Comfort(ComfortAdd):
    id: int

    # при помощи паттерна DataMapper из SQL Alchemy преобразуем в Pydantic схему
    model_config = ConfigDict(from_attributes=True)


class RoomsComfortAdd(BaseModel):
    room_id: int
    comfort_id: int

class RoomsComfort(RoomsComfortAdd):
    id: int