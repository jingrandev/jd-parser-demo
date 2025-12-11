from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.hr.services.jd_parser import JDParserService, get_jd_parser_service

router = APIRouter()


class JDInput(BaseModel):
    text: str


class JDOutput(BaseModel):
    role_title: str
    mission: str
    core_responsibilities: list[str]
    required_skills: list[str]


@router.post("/parse_jd", response_model=JDOutput)
async def parse_jd_endpoint(
    payload: JDInput,
    service: JDParserService = Depends(get_jd_parser_service),
) -> JDOutput:
    data = await service.parse(payload.text)
    return JDOutput(
        role_title=data.get("role_title", ""),
        mission=data.get("mission", ""),
        core_responsibilities=data.get("core_responsibilities", []),
        required_skills=data.get("required_skills", []),
    )
