from pydantic import BaseModel

# схема используется для добавления и обновления всех данных
# нет id т.к. мы вводим его сами (передаем в параметрах пути)
class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd): # наследуемся чтобы полностью соответствовать модели HotelsOrm, значит легко превратить в pydantic схему (вернуть)
    id: int

class HotelPatch(BaseModel):
    title: str | None = None # обязательно указывать значение по умолчанию иначе работать не будет
    location: str | None = None # обязательно указывать значение по умолчанию иначе работать не будет