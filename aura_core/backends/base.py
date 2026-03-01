from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from PIL import Image


class BaseLLMBackend(ABC):
    @abstractmethod
    def chat(self, message: str, history: List[Tuple[str, str]]) -> str: ...


class BaseImageGenBackend(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> tuple[Optional[Image.Image], str]: ...


class BaseImageEditBackend(ABC):
    @abstractmethod
    def edit(self, image: Image.Image, prompt: str) -> tuple[Optional[Image.Image], str]: ...
