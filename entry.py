from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from apps.routes import router as apps_router
from conf import setting
from libs.logging.logger import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(title=setting.APP_TITLE, debug=setting.DEBUG, lifespan=lifespan)

app.include_router(apps_router, prefix=setting.API_V1_PREFIX)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception on {path}: {exc_type}: {exc}",
        path=request.url.path,
        exc_type=exc.__class__.__name__,
        exc=exc,
    )
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "error_type": exc.__class__.__name__,
        },
    )
