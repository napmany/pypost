from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from typing import Any, List, Type, Union
from sqlalchemy.orm import selectinload
from enum import Enum
from sqlalchemy.sql import Select


class BaseRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session


def load_relations(
    stmt: Select,
    model: Type[Any],
    includes: List[Union[str, Enum]],
) -> Select:
    options = []
    if includes:
        for relation in includes:
            try:
                relation_name = (
                    relation.value if isinstance(relation, Enum) else relation
                )
                options.append(selectinload(getattr(model, relation_name)))
            except AttributeError:
                raise ValueError(f"Invalid relation: {relation_name}")
    if options:
        stmt = stmt.options(*options)
    return stmt
