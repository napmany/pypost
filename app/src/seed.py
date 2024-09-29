import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.database import sessionmanager
from src.config.manager import get_settings
import src.models as models


async def seed_db():
    settings = get_settings()
    sessionmanager.init(settings.DB_POSTGRES_URI)

    async with sessionmanager.session() as session:
        # Create users
        user1 = models.User(name="Alice")
        user2 = models.User(name="Bob")
        session.add_all([user1, user2])
        await session.flush()  # This will assign IDs to the users

        # Create tags
        tag1 = models.Tag(name="Python")
        tag2 = models.Tag(name="FastAPI")
        session.add_all([tag1, tag2])
        await session.flush()  # This will assign IDs to the tags

        # Create post
        post1 = models.Post(
            title="First Post",
            content="Content",
            status="draft",
            user_id=user1.id,
            tags=[tag1, tag2],
        )
        session.add(post1)

        await session.commit()

    await sessionmanager.close()


if __name__ == "__main__":
    asyncio.run(seed_db())
