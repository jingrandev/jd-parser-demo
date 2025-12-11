from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from conf import setting
from apps.routes import router as apps_router


app = FastAPI(title=setting.APP_TITLE, debug=setting.DEBUG)


app.include_router(apps_router, prefix=setting.API_V1_PREFIX)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "error_type": exc.__class__.__name__,
        },
    )
