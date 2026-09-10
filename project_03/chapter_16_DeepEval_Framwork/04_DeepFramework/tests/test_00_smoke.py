"""Smoke tests: prove the wiring before spending a single judge token.

Everything here is cheap. If these fail, every metric downstream would fail
too, but for an infrastructure reason rather than a quality one, and the
error message would be much harder to read.
"""
import pytest

from targets.chatbot import ChatbotClient


@pytest.mark.smoke
def test_chatbot_is_reachable():
    health = ChatbotClient().health()
    assert health["status"] == "ok"


@pytest.mark.smoke
def test_chatbot_is_not_in_mock_mode():
    """A green suite against the mock responder would mean nothing."""
    reply = ChatbotClient().chat("What is your refund window?")
    assert reply.mode == "live", (
        f"chatbot answered in '{reply.mode}' mode - set GROQ_API_KEY and "
        f"CHATBOT_MODEL in the chatbot's .env"
    )
    assert reply.reply.strip()


@pytest.mark.smoke
def test_judge_is_configured():
    from llm_providers.judge import build_judge

    out, _ = build_judge().generate("Reply with the single word: ok")
    assert isinstance(out, str) and out.strip()
