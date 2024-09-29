import sqlalchemy

from src.models import User
from src.repository.base import BaseRepository
from src.utilities.exceptions.database import EntityDoesNotExist
from src.schemas import UserFilter
from src.repository.base import load_relations


class UserRepository(BaseRepository):
    async def read_user_by_id(self, id: int, filter: UserFilter) -> User:
        stmt = sqlalchemy.select(User).where(User.id == id)
        stmt = load_relations(stmt, User, filter.include)

        query = await self.async_session.execute(statement=stmt)
        user = query.scalar()

        if not user:
            raise EntityDoesNotExist(f"User with id `{id}` does not exist!")

        return user
