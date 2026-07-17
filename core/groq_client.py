"""
NOVARYN Groq Client
Centralized Groq API wrapper.
"""

from __future__ import annotations

import time
from typing import List, Dict

from groq import Groq

from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

from core.logger import get_logger
from core.exceptions import (
    ConfigurationError,
    APIError,
)

logger = get_logger("groq")


class GroqClient:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        if not GROQ_API_KEY:
            raise ConfigurationError(
                "GROQ_API_KEY not found."
            )

        self.client = Groq(api_key=GROQ_API_KEY)

        self.model = GROQ_MODEL

        self._initialized = True

        logger.info(f"Groq initialized ({self.model})")

    # ----------------------------------------------------
    # Chat Completion
    # ----------------------------------------------------

    def chat(
        self,
        messages: List[Dict],
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ) -> str:

        retries = 3

        for attempt in range(retries):

            try:

                response = self.client.chat.completions.create(

                    model=self.model,

                    messages=messages,

                    temperature=temperature,

                    max_tokens=max_tokens,

                )

                return response.choices[0].message.content

            except Exception as e:

                logger.warning(
                    f"Attempt {attempt+1}/{retries}: {e}"
                )

                time.sleep(2)

        raise APIError(
            "Failed to communicate with Groq API."
        )

    # ----------------------------------------------------
    # Streaming
    # ----------------------------------------------------

    def stream(
        self,
        messages: List[Dict],
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ):

        try:

            stream = self.client.chat.completions.create(

                model=self.model,

                messages=messages,

                temperature=temperature,

                max_tokens=max_tokens,

                stream=True,

            )

            for chunk in stream:

                delta = chunk.choices[0].delta.content

                if delta:
                    yield delta

        except Exception as e:

            logger.exception(e)

            raise APIError(str(e))

    # ----------------------------------------------------
    # Health Check
    # ----------------------------------------------------

    def health(self) -> bool:

        try:

            self.chat(
                [
                    {
                        "role": "user",
                        "content": "Hello"
                    }
                ],
                max_tokens=5
            )

            return True

        except Exception:

            return False

    # ----------------------------------------------------
    # Model
    # ----------------------------------------------------

    def get_model(self):

        return self.model


# ======================================================
# Singleton Instance
# ======================================================

groq_client = GroqClient()