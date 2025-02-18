from datetime import datetime

from pydantic import EmailStr

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class UsersOrm(Base):
    __tablename__ ="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    # create_at: Mapped[datetime | None]