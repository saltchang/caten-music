from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import get_settings
from app.api.routers import auth, files, health, invitation, reports, songlists, songs, users
from app.config.settings import Settings
from app.repository.database import create_engine_from_url, create_session_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = app.state.settings
    engine = create_engine_from_url(settings.database_url)
    create_session_factory(engine)

    yield

    await engine.dispose()


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = get_settings()

    app = FastAPI(title='Caten Music API', lifespan=lifespan)
    app.state.settings = settings

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(songs.router)
    app.include_router(songlists.router)
    app.include_router(users.router)
    app.include_router(invitation.router)
    app.include_router(reports.router)
    app.include_router(files.router)

    return app
