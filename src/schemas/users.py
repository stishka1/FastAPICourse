from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

# конвертация из 1 pydantic схемы (UserRequestAdd) в другую схему (UserAdd)
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

# отдаем все кроме пароля (что никому никуда его не показывать)
class User(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

# класс только для логина юзера
class LoginUser(User):
    hashed_password: str

    # при помощи паттерна DataMapper из SQL Alchemy преобразуем в Pydantic схему
    model_config = ConfigDict(from_attributes=True)
