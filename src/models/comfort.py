from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


# справочник удобств для номеров
class ComfortOrm(Base):
    __tablename__ ="comfort"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

# many to many связь (комнаты и все удобства в ней)
class RoomsComfortOrm(Base):
    __tablename__ ="rooms_comfort"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    comfort_id: Mapped[int] = mapped_column(ForeignKey("comfort.id"))