from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def create_engine_from_url(url: str) -> AsyncEngine:
    global _engine
    _engine = create_async_engine(url, echo=False)
    return _engine


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    global _session_factory
    _session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return _session_factory


async def get_session() -> AsyncGenerator[AsyncSession]:
    if _session_factory is None:
        raise RuntimeError(
            'Session factory not initialized. Call create_engine_from_url and create_session_factory first.'
        )
    async with _session_factory() as session:
        yield session
