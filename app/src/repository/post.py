import typing

import sqlalchemy

from src.models import Post
from src.repository.base import BaseRepository
from src.utilities.exceptions.database import EntityDoesNotExist
from src.schemas import PostFilter, PostsFilter
from src.repository.base import load_relations


class PostRepository(BaseRepository):
    async def read_posts(self, filter: PostsFilter) -> typing.Sequence[Post]:
        stmt = sqlalchemy.select(Post)
        stmt = load_relations(stmt, Post, filter.include)

        if filter.status:
            stmt = stmt.where(Post.status == filter.status)

        query = await self.async_session.execute(statement=stmt)

        return query.scalars().all()

    async def read_post_by_id(self, id: int, filter: PostFilter) -> Post:
        stmt = sqlalchemy.select(Post).where(Post.id == id)
        stmt = load_relations(stmt, Post, filter.include)

        query = await self.async_session.execute(statement=stmt)
        post = query.scalar()

        if not post:
            raise EntityDoesNotExist(f"Post with id `{id}` does not exist!")

        return post
