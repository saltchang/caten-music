from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def create_engine_from_url(url: str) -> AsyncEngine:
    """Create and cache the async SQLAlchemy engine.

    Args:
        url: Database connection URL.

    Returns:
        The created AsyncEngine instance.
    """
    global _engine
    _engine = create_async_engine(url, echo=False)
    return _engine


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create and cache the async session factory.

    Args:
        engine: The AsyncEngine to bind sessions to.

    Returns:
        The created session factory.
    """
    global _session_factory
    _session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return _session_factory


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Yield an async database session.

    Raises:
        RuntimeError: If session factory has not been initialized.
    """
    if _session_factory is None:
        raise RuntimeError(
            'Session factory not initialized. Call create_engine_from_url and create_session_factory first.'
        )
    async with _session_factory() as session:
        yield session
