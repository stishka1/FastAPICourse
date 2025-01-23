from src.models.comfort import ComfortOrm
from src.repos.base import BaseRepository
from src.schemas.comfort import Comfort


class ComfortRepository(BaseRepository):
    model = ComfortOrm
    schema = Comfort
