from datetime import date
from pydantic import BaseModel

class BookingAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int