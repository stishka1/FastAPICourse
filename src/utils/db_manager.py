# реализация своего асинхронного контекстного менеджера
# Для чего это вообще нужно?
# Избавились от работы с репозиториями (лишние импорты)
# Избавились от постоянного вызова контектсного менедждера async_session_manager()
# Внедрили ролбек (откат изменений в случае ошибки)
# Вся работа с БД и сессиями тут

from src.repos.hotels import HotelsRepository
from src.repos.rooms import RoomsRepository
from src.repos.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()