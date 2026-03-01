from __future__ import annotations

from typing import List, Tuple

import requests


class OllamaLLMBackend:
    def __init__(self, host: str, model: str):
        self.host = host.rstrip("/")
        self.model = model

    def chat(self, message: str, history: List[Tuple[str, str]]) -> str:
        url = f"{self.host}/api/chat"

        messages = []
        for u, a in history[-20:]:
            messages.append({"role": "user", "content": u})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": message})

        try:
            r = requests.post(
                url,
                json={"model": self.model, "messages": messages, "stream": False},
                timeout=120,
            )
            r.raise_for_status()
            data = r.json()
            return (data.get("message") or {}).get("content") or "(No response)"
        except Exception as e:
            return (
                "I couldn't reach Ollama. Make sure it's running, then set OLLAMA_HOST and OLLAMA_MODEL. "
                f"Error: {e}"
            )
