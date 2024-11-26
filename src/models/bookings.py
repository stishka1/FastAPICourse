from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, MappedColumn
from sqlalchemy import String, ForeignKey


class BookingsOrm(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property # декоратор для создания аттрибута
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days




























