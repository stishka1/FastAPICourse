from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.schemas.bookings import BookingAdd


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingAdd
