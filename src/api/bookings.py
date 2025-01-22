from fastapi import APIRouter, Request

from src.api.dependencies import DBDep, UserDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.auth import AuthService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

# принцип такой: много параметров передаем в pydantic схему (создаем ее)
# Таким образом в Body будет валидация пользовательских данных от pydantic
# недостающие данные указываем в другой схеме (2 схемы)
# соединяем 2 схемы путем раскрытия словаря или метода .model_dump()
@router.post("", summary="Добавить бронирование номера")
async def add_booking(db: DBDep, user_id: UserDep, bookingData: BookingAddRequest):
    room_info = await db.rooms.get_one_or_none(id=bookingData.room_id)
    room_price = room_info.price

    _booking_data = BookingAdd(user_id=user_id, price=room_price, **bookingData.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "200", "data": booking}

@router.get("", summary="Получить бронирования всех пользователей")
async def get_all_bookings(db: DBDep):
    all_bookings = await db.bookings.get_all()
    return {"status": "200", "data": all_bookings}

@router.get("/me", summary="Получить мои бронирования")
async def get_my_bookings(db: DBDep, user_id: UserDep):
    my_bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "200", "data": my_bookings}