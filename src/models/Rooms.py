from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class RoomsOrm(Base):
    __tablename__ ="rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    # для связки 2х моделей Rooms (Комнаты) и Comfort (удобства) - через relationship
    # comforts - название любое для модели comforts.py -> back_populates
    comforts: Mapped[list["ComfortOrm"]] = relationship(
        back_populates="rooms",
        secondary="rooms_comfort",
    )