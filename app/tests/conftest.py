import asgi_lifespan
import fastapi
import httpx
import pytest
from src.main import init_app
from src.database import get_db, sessionmanager
from src.models import User, Post, Comment, Tag

@pytest.fixture(name="test_app")
def test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """
    return init_app(init_db=False)


@pytest.fixture(name="initialize_test_application")
async def initialize_test_application(test_app: fastapi.FastAPI) -> fastapi.FastAPI:  # type: ignore
    async with asgi_lifespan.LifespanManager(test_app):
        yield test_app


@pytest.fixture(scope="function", autouse=True)
async def connection_test():
    pg_host = "db_test"
    pg_port = 5432
    pg_user = "test"
    pg_db = "test"
    pg_password = "test"

    connection_str = f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    sessionmanager.init(connection_str)
    yield
    await sessionmanager.close()
        
        
@pytest.fixture(scope="function", autouse=True)
async def create_tables():
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)
    async with sessionmanager.session() as session:
        await seed_database(session)
        
        
@pytest.fixture(scope="function", autouse=True)
async def session_override(test_app):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    test_app.dependency_overrides[get_db] = get_db_override


@pytest.fixture(name="async_client")
async def async_client(initialize_test_application: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with httpx.AsyncClient(
        app=initialize_test_application,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
        
        
async def seed_database(session):
    user = User(id=1, name='tester')
    session.add(user)
    await session.flush()
    
    tag = Tag(id=1, name='test')
    session.add(tag)
    await session.flush()
        
    post = Post(id=1, title='test', content='test', status='draft', user_id=user.id, tags=[tag])
    session.add(post)
    await session.flush() 
    
    post2 = Post(id=2, title='test2', content='test2', status='some', user_id=user.id, tags=[tag])
    session.add(post2)
    await session.flush() 
    
    comment = Comment(id=1, content='test', user_id=user.id, post_id=post.id)
    session.add(comment)
    await session.flush() 
    
    await session.commit()
