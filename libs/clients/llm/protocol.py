from dataclasses import dataclass
from typing import Any, Awaitable, Dict, List, Optional, Protocol


@dataclass
class ChatResult:
    ok: bool
    model: str
    content: str
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None


class LLMClient(Protocol):
    def chat(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.7,
    ) -> Awaitable[ChatResult]:
        ...
