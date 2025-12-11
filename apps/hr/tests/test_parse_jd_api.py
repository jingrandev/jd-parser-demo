import pytest
from fastapi.testclient import TestClient

from apps.hr.services.jd_parser import JDParserService, get_jd_parser_service
from entry import app


class DummyJDParserService(JDParserService):
    async def parse(self, jd_text: str) -> dict:  # type: ignore[override]
        return {
            "role_title": "Backend Engineer",
            "mission": "Build APIs and AI workflows",
            "core_responsibilities": ["Design backend services"],
            "required_skills": ["Python", "FastAPI"],
        }


class ErrorJDParserService(JDParserService):
    async def parse(self, jd_text: str) -> dict:  # type: ignore[override]
        raise RuntimeError("parse failed")


client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def reset_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def test_parse_jd_api_success():
    app.dependency_overrides[get_jd_parser_service] = lambda: DummyJDParserService(  # type: ignore[assignment]
        llm_client=None  # type: ignore[arg-type]
    )

    payload = {"text": "We are hiring a backend engineer."}

    response = client.post("/api/v1/hr/parse_jd", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["role_title"] == "Backend Engineer"
    assert data["mission"] == "Build APIs and AI workflows"
    assert data["core_responsibilities"] == ["Design backend services"]
    assert data["required_skills"] == ["Python", "FastAPI"]


def test_parse_jd_api_runtime_error_triggers_generic_handler():
    app.dependency_overrides[get_jd_parser_service] = lambda: ErrorJDParserService(  # type: ignore[assignment]
        llm_client=None  # type: ignore[arg-type]
    )

    payload = {"text": "We are hiring a backend engineer."}

    response = client.post("/api/v1/hr/parse_jd", json=payload)

    assert response.status_code == 500
    data = response.json()
    assert data["message"] == "Internal server error"
    assert data["error_type"] == "RuntimeError"


def test_parse_jd_api_empty_text_validation_error():
    payload = {"text": ""}

    response = client.post("/api/v1/hr/parse_jd", json=payload)

    assert response.status_code == 422
