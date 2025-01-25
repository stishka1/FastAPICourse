from src.models.comfort import ComfortOrm, RoomsComfortOrm
from src.repos.base import BaseRepository
from src.schemas.comfort import Comfort, RoomsComfort


class ComfortRepository(BaseRepository):
    model = ComfortOrm
    schema = Comfort


class RoomsComfortRepository(BaseRepository):
    model = RoomsComfortOrm
    schema = RoomsComfort
