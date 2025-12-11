from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI

from conf import setting
from .protocol import ChatResult, LLMClient


class OpenAIClient(LLMClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        key = api_key or setting.OPENAI_API_KEY
        if key is None:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set and no api_key was provided")

        self._client = AsyncOpenAI(
            api_key=key,
            base_url=base_url or setting.OPENAI_BASE_URL,
        )

    async def chat(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.7,
    ) -> ChatResult:
        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=False,
            )

            content = response.choices[0].message.content
            usage = getattr(response, "usage", None)

            return ChatResult(
                ok=True,
                model=model,
                content=content,
                usage=usage,
                raw=response,
            )
        except Exception as exc:
            return ChatResult(
                ok=False,
                model=model,
                content=f"LLM request failed: {exc}",
                usage=None,
                raw=exc,
            )