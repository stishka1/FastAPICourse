from typing import Annotated
from fastapi import Query, Depends
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, description="Страница", ge=1)] # тут мы разжевали fastapi с помощью типизации annotated что мы передаем, чтобы он все это распознал
    per_page: Annotated[int | None, Query(None, description = "Количество", ge=1, lt=50)]


PaginationDep = Annotated[PaginationParams, Depends()]