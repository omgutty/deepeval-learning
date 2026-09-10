"""Client for Subsystem A - the ShopSphere chatbot (the app under test).

The framework never imports the chatbot's code. It talks to the running
service over HTTP, exactly as a real user would, so what we score is the
deployed behaviour and not a unit-tested internal function.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from token_meter import METER

load_dotenv()

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8201").rstrip("/")
TIMEOUT = float(os.getenv("CHATBOT_TIMEOUT", "60"))


@dataclass
class ChatReply:
    reply: str
    model: str
    mode: str


class ChatbotClient:
    def __init__(self, base_url: str = CHATBOT_URL):
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict:
        r = requests.get(f"{self.base_url}/health", timeout=10)
        r.raise_for_status()
        return r.json()

    def is_up(self) -> bool:
        try:
            return self.health().get("status") == "ok"
        except Exception:  # noqa: BLE001 - any failure means "not usable"
            return False

    def chat(self, message: str, history: list[dict] | None = None) -> ChatReply:
        payload: dict = {"message": message}
        if history:
            payload["history"] = history
        r = requests.post(f"{self.base_url}/chat", json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        usage = data.get("usage")
        if usage:
            METER.record(
                "target",
                usage.get("prompt_tokens", 0),
                usage.get("completion_tokens", 0),
            )
        return ChatReply(
            reply=data.get("reply") or "",
            model=data.get("model", "unknown"),
            mode=data.get("mode", "unknown"),
        )
