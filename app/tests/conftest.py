import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.base import Base, User
from app.schemas.user import UserCreate
from app.database.user import user_crud
from app.core.db import get_async_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession,
                                   expire_on_commit=False)


@pytest_asyncio.fixture(loop_scope='session', autouse=True)
async def setub_test_db():
    """Создаем асинхронную БД."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(loop_scope='function')
async def async_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(loop_scope='session')
async def test_app(async_session: AsyncSession):
    async def override_get_db():
        yield async_session
    app.dependency_overrides[get_async_session] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(loop_scope='function')
async def async_client(test_app):
    async with AsyncClient(
         transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture()
async def get_user_schema():
    return UserCreate(email='test@mail.ru', password='test')


@pytest_asyncio.fixture()
async def get_or_register_user(
        get_user_schema: UserCreate,
        async_client: AsyncClient,
        async_session: AsyncSession):
    user: User | None = await user_crud.get_user(
        get_user_schema.email, async_session)
    auth_data: dict[str, str] = dict()
    if user is None:
        response = await async_client.post(
            'auth/register', json=get_user_schema.dict())
        data = response.json()
        auth_data['username'] = data['email']
        auth_data['password'] = get_user_schema.password
    else:
        auth_data['username'] = user.email
        auth_data['password'] = get_user_schema.password
    return auth_data


@pytest_asyncio.fixture()
async def get_auth_header(
        get_or_register_user: dict[str, str], async_client: AsyncClient):
    response = await async_client.post(
        'auth/jwt/login', data=get_or_register_user)
    data = response.json()
    return {"Authorization": f"Bearer {data['access_token']}"}
