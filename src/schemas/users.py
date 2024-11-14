from pydantic import BaseModel, EmailStr, ConfigDict


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str

# конвертация из 1 pydantic схемы (UserRequestAdd) в другую схему (UserAdd)
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    username: str

# отдаем все кроме пароля (что никому никуда его не показывать)
class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    username: str

    # при помощи паттерна DataMapper из SQL Alchemy преобразуем в Pydantic схему
    model_config = ConfigDict(from_attributes=True)
