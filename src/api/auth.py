from http.client import responses

from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext

from src.api.dependencies import UserDep
from src.database import async_session_maker
from src.repos.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Пользователи"])

@router.post("/register")
async def register(data: UserRequestAdd):

    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, first_name=data.first_name, last_name=data.last_name, username=data.username)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "200"}

@router.post("/login")
async def login(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        try:
            user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
            if not user:
                raise HTTPException(status_code=401, detail='Пользователь с таким email не найден!')
            if not AuthService().verify_password(data.password, user.hashed_password):
                raise HTTPException(status_code=401, detail='Пароль неверный!')
        except:
            raise HTTPException(status_code=401, detail='Пользователь с таким email не найден!')
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.get("/about_me", summary="Информация обо мне")
async def get_token(user_id: UserDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user

@router.post('/logout', summary="Выйти из системы")
async  def logout(response: Response):
    response.delete_cookie("access_token")
    return {"detail": "успешно вышли"}