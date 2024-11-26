from datetime import date

from fastapi import APIRouter, Request

from src.api.dependencies import DBDep, UserDep
from src.schemas.bookings import BookingAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("", summary="Добавить бронирование номера")
async def add_booking(db: DBDep, room_id: int, date_from: date, date_to: date, user_id: UserDep):
    room_info = await db.rooms.get_one_or_none(id=room_id)

    total = room_info.price * (date_to - date_from).days
    booking_data = {
        "room_id": room_id,
        "user_id": user_id,
        "date_from": date_from,
        "date_to": date_to,
        "price": total
    }
    _booking_data = BookingAdd(**booking_data)
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "200", "data": booking}