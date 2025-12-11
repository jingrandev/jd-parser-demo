from fastapi import APIRouter

from apps.hr.endpoints.parse_jd import router as parse_jd_router


router = APIRouter(prefix="/hr", tags=["hr"])

router.include_router(parse_jd_router)
