from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import async_session_maker
from src.repos.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

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