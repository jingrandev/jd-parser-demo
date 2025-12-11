from fastapi import APIRouter

from apps.hr.routes import router as hr_router


router = APIRouter()

router.include_router(hr_router)

