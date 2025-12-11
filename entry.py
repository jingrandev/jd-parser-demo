from fastapi import FastAPI

from conf import setting
from apps.routes import router as apps_router


app = FastAPI(title=setting.APP_TITLE, debug=setting.DEBUG)


app.include_router(apps_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
