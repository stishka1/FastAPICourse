from pydantic import BaseModel

class Hotel(BaseModel):
    title: str
    location: str

class HotelPatch(BaseModel):
    title: str | None = None # обязательно указывать по умолчанию иначе работать не будет
    location: str | None = None # обязательно указывать по умолчанию иначе работать не будет