from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import get_settings
from app.api.routers import admin, auth, files, health, invitation, reports, songlists, songs
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

    app.include_router(health.router, prefix='/api')
    app.include_router(auth.router, prefix='/api')
    app.include_router(songs.router, prefix='/api')
    app.include_router(songlists.router, prefix='/api')
    app.include_router(admin.router, prefix='/api')
    app.include_router(invitation.router, prefix='/api')
    app.include_router(reports.router, prefix='/api')
    app.include_router(files.router, prefix='/api')

    return app
