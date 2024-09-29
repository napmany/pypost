from fastapi import FastAPI

from src.database import Base
from src.database import sessionmanager
from src.api.routers import posts, users
from contextlib import asynccontextmanager
from src.config.manager import get_settings
from src.api.middlewares.query_string import FlattenQueryStringLists


def init_app(init_db=True):
    lifespan = None

    settings = get_settings()

    if init_db:
        db_uri = settings.DB_POSTGRES_URI
        sessionmanager.init(db_uri)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Create database tables
            async with sessionmanager.connect() as conn:
                await conn.run_sync(Base.metadata.create_all)
            yield
            # Close database connection
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(title="FastAPI server", lifespan=lifespan)

    # Include API routers
    app.include_router(posts.router, prefix="/api")
    app.include_router(users.router, prefix="/api")

    app.add_middleware(FlattenQueryStringLists)

    return app
