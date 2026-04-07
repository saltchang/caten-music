from collections.abc import AsyncGenerator
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from app import create_app
from app.api.dependencies import get_db_session, get_file_download_service, get_mail_service, get_settings
from app.config.settings import Settings
from app.core.entities.invitation_code import InvitationCode
from app.core.entities.user import User
from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from app.repository.invitation_repository import SqlAlchemyInvitationRepository
from app.repository.user_profile_repository import SqlAlchemyUserProfileRepository
from app.repository.user_repository import SqlAlchemyUserRepository
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.fixture
def settings() -> Settings:
    return Settings(
        database_url='sqlite+aiosqlite://',
        secret_key='test-secret-key-long-enough-for-hmac-sha256',
        hash_salt='test-hash-salt',
        testing=True,
    )


@pytest.fixture
async def async_engine(settings: Settings):
    # Models use schema='public' for PostgreSQL production.
    # SQLite has no schema concept, so schema_translate_map
    # rewrites 'public.users' → 'users' in generated SQL.
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        execution_options={'schema_translate_map': {'public': None}},
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_session(async_engine) -> AsyncGenerator[AsyncSession]:
    from app.repository.models import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def _shared_db(async_engine):
    """Shared connection for API integration tests.

    In-memory SQLite is per-connection, so the test setup (api_session)
    and the FastAPI app (client) must share the same connection to see
    each other's data.
    """
    from app.repository.models import Base

    conn = await async_engine.connect()
    await conn.begin()
    await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=conn, class_=AsyncSession, expire_on_commit=False)

    yield session_factory

    await conn.close()


@pytest.fixture
async def api_session(_shared_db: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession]:
    """Session for setting up test data in API integration tests."""
    async with _shared_db() as session:
        yield session


@pytest.fixture
def mock_file_service() -> MagicMock:
    mock = MagicMock()
    mock.get_ppt_url = AsyncMock(return_value=None)
    mock.get_sheet_url = AsyncMock(return_value=None)
    return mock


@pytest.fixture
async def client(
    _shared_db: async_sessionmaker[AsyncSession],
    settings: Settings,
    mock_file_service: MagicMock,
) -> AsyncGenerator[AsyncClient]:
    mock_mail_service = MagicMock()

    async def override_get_db_session():
        async with _shared_db() as session:
            yield session

    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_mail_service] = lambda: mock_mail_service
    app.dependency_overrides[get_file_download_service] = lambda: mock_file_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


@pytest.fixture
def password_hasher(settings: Settings) -> Sha256PasswordHasher:
    return Sha256PasswordHasher(salt=settings.hash_salt)


@pytest.fixture
def token_service(settings: Settings) -> JwtTokenService:
    return JwtTokenService(
        secret_key=settings.secret_key,
        algorithm=settings.jwt_algorithm,
        access_token_expire_minutes=settings.jwt_access_token_expire_minutes,
        refresh_token_expire_minutes=settings.jwt_refresh_token_expire_minutes,
        activation_token_expire_minutes=settings.jwt_activation_token_expire_minutes,
    )


async def create_test_invitation_code(session: AsyncSession, created_by: int = 1) -> InvitationCode:
    repo = SqlAlchemyInvitationRepository(session)
    invitation = InvitationCode(
        id=0,
        code='TESTCODE1234',
        created_by=created_by,
        expires_at=datetime.now() + timedelta(hours=48),
    )
    return await repo.create(invitation)


async def create_test_user(
    session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    username: str = 'testuser',
    email: str = 'test@example.com',
    displayname: str = 'Test User',
    password: str = 'Test1234!',
    is_authenticated: bool = True,
    is_active: bool = True,
    is_admin: bool = False,
    is_manager: bool = False,
) -> User:
    user_repo = SqlAlchemyUserRepository(session)
    profile_repo = SqlAlchemyUserProfileRepository(session)

    user = User(
        id=0,
        username=username,
        email=email,
        password_hash=password_hasher.hash(password),
        displayname=displayname,
        is_authenticated=is_authenticated,
        is_active=is_active,
        is_admin=is_admin,
        is_manager=is_manager,
    )
    created_user = await user_repo.create(user)

    from app.core.entities.user_profile import UserProfile

    profile = UserProfile(id=0, user_id=created_user.id)
    await profile_repo.create(profile)

    return created_user


async def get_auth_token(
    session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
    username: str = 'testuser',
    email: str = 'test@example.com',
    is_admin: bool = False,
    is_manager: bool = False,
) -> tuple[str, User]:
    user = await create_test_user(
        session,
        password_hasher,
        username=username,
        email=email,
        is_admin=is_admin,
        is_manager=is_manager,
    )
    access_token = token_service.create_access_token(user.id)
    return access_token, user
