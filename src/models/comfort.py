from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


# справочник удобств для номеров
class ComfortOrm(Base):
    __tablename__ ="comfort"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    # для связки 2х моделей Rooms (Комнаты) и Comfort (удобства) - через relationship
    # rooms - название любое для модели rooms.py -> back_populates
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="comforts",
        secondary="rooms_comfort",
    )

# many to many связь (комнаты и все удобства в ней)
class RoomsComfortOrm(Base):
    __tablename__ ="rooms_comfort"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    comfort_id: Mapped[int] = mapped_column(ForeignKey("comfort.id"))