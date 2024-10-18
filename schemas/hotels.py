from pydantic import BaseModel

class Hotel(BaseModel):
    title: str
    name: str

class HotelPatch(BaseModel):
    title: str | None = None # обязательно указывать по умолчанию иначе работать не будет
    name: str | None = None # обязательно указывать по умолчанию иначе работать не будет