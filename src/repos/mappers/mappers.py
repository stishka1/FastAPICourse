from src.models.bookings import BookingsOrm
from src.models.comfort import ComfortOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repos.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.comfort import Comfort
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.schemas.users import User


# маппер позволяет не привязывая модель алхимии и pydantic взаимодействовать и
# превращать данные из 1 сущности в другую
class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel

class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking

class ComfortDataMapper(DataMapper):
    db_model = ComfortOrm
    schema = Comfort