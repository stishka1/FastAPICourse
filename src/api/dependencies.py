# Определяет функции, обеспечивающие зависимости для эндпоинтов (например получение user id).

from fastapi import HTTPException, Request
from typing import Annotated
from fastapi import Query, Depends
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Страница", ge=1)] # тут мы разжевали fastapi с помощью типизации annotated что мы передаем, чтобы он все это распознал
    per_page: Annotated[int | None, Query(None, description = "Количество", ge=1, lt=50)]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None) # None вместо текста чтобы здесь выполнить ошибку иначе перескочит на ошибку в decode_token (Неверный токен)
    if not token:
        raise HTTPException(status_code=401, detail='Токен не найден')
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return  data.get('user_id', 'В токене нет user_id')



UserDep = Annotated[int, Depends(get_current_user_id)]

# def get_db_manager():
#     return DBManager(session_factory=async_session_maker())


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]