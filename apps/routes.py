from fastapi import APIRouter

from apps.hr.routes import router as hr_router


router = APIRouter()

router.include_router(hr_router)


@router.get("/health")
async def health_check():
    return {"status": "ok"}

