"""
LLM-as-a-judge evaluation test (Groq + DeepEval).

Flow:
  1. Ask a model served by Groq a question  -> the "model under test"
  2. Wrap the question/answer in an LLMTestCase
  3. Score it with two DeepEval metrics    -> the "judge"
  4. assert_test() fails the pytest run if any metric misses its threshold

The model under test and the judge are deliberately different providers:
Groq answers, OpenRouter grades (see .env -> USE_OPENROUTER_MODEL).
"""

# --- Config -----------------------------------------------------------------
GROQ_MODEL = "qwen/qwen3.8-27b"        # model we are evaluating (served by Groq)
JUDGE_MODEL = "openai/gpt-oss-120b"    # model that scores the answer (served by OpenRouter)

# --- Imports ----------------------------------------------------------------
import os  # read API keys from environment variables

from dotenv import load_dotenv  # load variables from the local .env file into os.environ
from openai import OpenAI  # OpenAI SDK client; Groq is OpenAI-compatible, so we just point it at Groq's URL

from deepeval.metrics import (
    AnswerRelevancyMetric,  # judge: does the answer actually address the question?
    HallucinationMetric,    # judge: does the answer contradict the given context?
)
from deepeval.test_case import LLMTestCase  # container holding input / actual_output / expected_output / context
from deepeval import assert_test  # runs the metrics and asserts every threshold is met (pytest-friendly)

load_dotenv()  # actually loads .env, so os.getenv() below sees the keys

# Client used to call the MODEL UNDER TEST. Groq exposes an OpenAI-compatible
# API, so the standard OpenAI SDK works once we override base_url.
# NOTE: the key lives in OPENAI_API_KEY (a Groq "gsk_..." key) — the variable
# name is only the SDK's conventional env var, not the provider.
groq = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def llm_response(question):
    """Ask GROQ_MODEL one question and return its raw answer text."""
    response = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": question}],
        # temperature=0 keeps the answer stable so the score below is
        # reproducible. The judge is still non-deterministic; this only
        # pins the thing under test.
        temperature=0,
    )
    return response.choices[0].message.content.strip()



# The question asked once at import time; the answer is reused by the test below.
question = "what is 2+2? reply with just the number"
answer = llm_response(question)
print(f"\n[Groq {GROQ_MODEL}] -> {answer!r}\n")


def test_qwen_with_judge_openai():
    # LLMTestCase is the unit DeepEval scores: the prompt, what the model said,
    # what we expected, and the ground-truth context the judge may check against.
    case = LLMTestCase(
        input=question,
        actual_output=answer,
        expected_output="4",
        context=["Basic arithmetic fact: 2 + 2 = 4"],
    )

    # Each metric is an LLM-as-a-judge call. `model=JUDGE_MODEL` sends scoring to
    # OpenRouter; thresholds decide pass/fail (relevancy must be high,
    # hallucination low).
    metrics = [
        AnswerRelevancyMetric(threshold=0.8, model=JUDGE_MODEL),
        HallucinationMetric(threshold=0.3, model=JUDGE_MODEL),
    ]

    # Runs both metrics and raises if any score misses its threshold -> pytest fails.
    assert_test(case, metrics)