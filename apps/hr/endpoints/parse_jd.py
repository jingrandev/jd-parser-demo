from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class JDInput(BaseModel):
    text: str


class JDOutput(BaseModel):
    role_title: str
    mission: str
    core_responsibilities: List[str]
    required_skills: List[str]


@router.post("/parse_jd", response_model=JDOutput)
async def parse_jd_endpoint(payload: JDInput) -> JDOutput:
    return JDOutput(
        role_title="Backend Engineer",
        mission="Build APIs and AI workflows",
        core_responsibilities=[
            "Design APIs",
            "Integrate LLM APIs",
            "Build pipelines",
        ],
        required_skills=[
            "Python",
            "FastAPI",
            "LLM usage",
        ],
    )

