import json

import pytest

from apps.hr.services.jd_parser import JDParserService
from libs.clients.llm.protocol import ChatResult, LLMClient


class DummyLLMClient(LLMClient):
    async def chat(self, model: str, messages, temperature: float = 0.7) -> ChatResult:
        data = {
            "role_title": "Backend Engineer",
            "mission": "Build APIs and AI workflows",
            "core_responsibilities": ["Design backend services"],
            "required_skills": ["Python", "FastAPI"],
        }
        return ChatResult(
            ok=True,
            model=model,
            content=json.dumps(data),
            usage=None,
            raw=None,
        )


@pytest.mark.asyncio
async def test_jd_parser_service_parse_with_dummy_llm():
    service = JDParserService(llm_client=DummyLLMClient())

    jd_text = "We are hiring a backend engineer to build APIs and AI workflows."

    result = await service.parse(jd_text)

    assert result["role_title"] == "Backend Engineer"
    assert result["mission"] == "Build APIs and AI workflows"
    assert result["core_responsibilities"] == ["Design backend services"]
    assert result["required_skills"] == ["Python", "FastAPI"]
