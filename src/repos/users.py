from pydantic import EmailStr
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.models.users import UsersOrm
from src.repos.mappers.mappers import UserDataMapper
from src.schemas.users import User, LoginUser


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return LoginUser.model_validate(model)