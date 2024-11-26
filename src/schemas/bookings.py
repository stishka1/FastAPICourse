from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

class Booking(BookingAdd):
    id: int

    # при помощи паттерна DataMapper из SQL Alchemy преобразуем в Pydantic схему
    model_config = ConfigDict(from_attributes=True)