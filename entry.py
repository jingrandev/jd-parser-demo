from fastapi import FastAPI

from apps.routes import router as apps_router


app = FastAPI()


app.include_router(apps_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
