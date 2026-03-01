from __future__ import annotations

from typing import Optional

from PIL import Image


class KleinImageEditBackend:
    def __init__(self):
        pass

    def edit(self, image: Image.Image, prompt: str) -> tuple[Optional[Image.Image], str]:
        if image is None:
            return None, "No input image provided."

        note = (
            "Klein 4B editing backend is scaffolded. Wire this to your chosen runtime (local server/API) "
            "and return the edited image."
        )
        return None, note
