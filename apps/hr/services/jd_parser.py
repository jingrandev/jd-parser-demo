# ruff: noqa: E501
import json
from functools import lru_cache
from typing import Any, Dict, List

from fastapi import Depends
from loguru import logger

from conf import setting
from libs.clients.llm.openai import OpenAIClient
from libs.clients.llm.protocol import LLMClient


class JDParserService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def parse(self, jd_text: str) -> Dict[str, Any]:
        prompt = """
        # Role
        You are a helpful assistant that extracts structured information from job descriptions.

        # Task
        You are given a JD text input, return structured dict object with keys: role_title, mission, core_responsibilities, required_skills.

        # Rules
        - return the json string that exactly starts with { and ends with }
        - use language the as same as the input
        - mission is a short summary in the job description, not the original text
        - the item of core_responsibilities and required_skills should be the name of the skill/ability, keep it simple and concise
            - e.g. "Building and consuming RESTful/GraphQL APIs" should be "RESTful/GraphQL APIs"
            - e.g. "Design and develop scalable backend services and APIs" should be "Design backend services"
        - core_responsibilities and required_skills must be arrays of strings
        - core_responsibilities and required_skills should contain no more than 6 items
        """

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": jd_text},
        ]

        result = await self.llm_client.chat(
            model=setting.OPENAI_MODEL,
            messages=messages,
            temperature=0.2,
        )

        if not result.ok:
            logger.error("JD parsing LLM call failed: {content}", content=result.content)
            raise RuntimeError(f"JD parsing failed: {result.content}")

        try:
            data = json.loads(result.content)
            return {
                "role_title": data.get("role_title", ""),
                "mission": data.get("mission", ""),
                "core_responsibilities": data.get("core_responsibilities", []),
                "required_skills": data.get("required_skills", []),
            }
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse LLM JSON response: {raw}", raw=result.content)
            raise RuntimeError("Failed to parse LLM JSON response") from exc


@lru_cache
def get_llm_client() -> LLMClient:
    return OpenAIClient()


def get_jd_parser_service(
    llm_client: LLMClient = Depends(get_llm_client),
) -> JDParserService:
    return JDParserService(llm_client=llm_client)
