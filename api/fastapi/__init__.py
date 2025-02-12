import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette import status

from config.env.general import APP_NAME
from config.logger import init_logger

from .error_handler import register_exception_handlers
from .router import (
    chat,
    evaluation,
    generation,
    health,
    prompting_job,
    prompting_method,
    technique,
    test_prompt,
    translation,
)

logger = logging.getLogger(__name__)

init_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        yield
    finally:
        logger.info("Application is shutting down...")


_app = FastAPI(
    title=APP_NAME,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)

register_exception_handlers(_app)

_app.include_router(chat.router)
_app.include_router(evaluation.router)
_app.include_router(generation.router)
_app.include_router(health.router)
_app.include_router(translation.router)
_app.include_router(technique.router)
_app.include_router(prompting_method.router)
_app.include_router(prompting_job.router)
_app.include_router(test_prompt.router)


@_app.get("/", include_in_schema=False)
async def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "OK", "server_time": datetime.now(UTC).isoformat()},
    )


@_app.get("/docs", include_in_schema=False)
async def get_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=APP_NAME,
        swagger_favicon_url="/favicon.ico",
    )


@_app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    if _app.openapi_schema:
        return _app.openapi_schema
    openapi_schema = get_openapi(
        title=APP_NAME,
        version="0.1.0",
        routes=_app.routes,
    )
    _app.openapi_schema = openapi_schema
    return _app.openapi_schema


http_api = _app
