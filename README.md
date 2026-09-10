# deepeval-learning

A hands-on learning repo for **[DeepEval](https://github.com/confident-ai/deepeval)** — an open-source, pytest-native framework for evaluating LLM applications.

The goal here isn't a product. It's a public log of me learning how to *measure* LLM output instead of eyeballing it: LLM-as-a-judge metrics, test cases, thresholds, and multi-provider setups.

---

## What's in here

| Project | Focus | Status |
|---|---|---|
| [`project_01/`](./project_01) | First setup: create a `uv` venv, install DeepEval, wire up a provider, write a first eval test | ✅ Working |
| [`project_02/`](./project_02) | Real evals: Answer Relevancy + Hallucination metrics, and grading a model served by **Groq** with a judge on **OpenRouter** | ✅ Working |

Each project is self-contained with its own `.venv/`, `.env`, and README.

---

## The idea in one picture

Every metric in DeepEval is an **LLM-as-a-judge**: you give it a question, the model's answer, and optionally the expected answer and context — then *another* LLM scores it and explains why.

```
   question ──► MODEL UNDER TEST ──► answer
                                        │
                                        ▼
                              LLMTestCase (input, actual_output,
                               expected_output, context)
                                        │
                                        ▼
                                  JUDGE LLM ──► score + pass/fail + reason
```

`assert_test()` turns that into a normal pytest assertion — a failing score fails the run.

---

## Projects in detail

### `project_01` — setup and first run

The "does my environment even work" project.

- Creates an isolated `uv` virtual environment (Python 3.13)
- Installs `deepeval` (`uv pip install -U deepeval`)
- Configures **OpenRouter** as the judge provider via `.env`
- Verifies the install and runs a first eval

**Verified:** DeepEval 4.2.1, `AnswerRelevancyMetric` scoring **1.0** against a **0.9** threshold.

### `project_02` — real metrics and a two-provider setup

Where it gets interesting: the model being tested and the model doing the judging are deliberately **different providers**.

| File | What it does |
|---|---|
| `test_01_Ans_Relevency.py` | Minimal Answer Relevancy eval (threshold 0.9), judge via OpenRouter |
| `test_02_Groq.py` | Asks a **Groq**-served model a question, then scores it with **Answer Relevancy** and **Hallucination** metrics judged via **OpenRouter** |
| `linked/post.md` | Write-up of the Groq experiment (LinkedIn post copy) |
| `linked/image-prompt.md` | Image-generation prompt for the post's cover art |
| `image.png` | Screenshot of the passing test run |

**Verified result** for `test_02_Groq.py`:

```
Pass Rate: 100.0% | Passed: 1 | Failed: 0

Answer Relevancy   1.00   PASSED   (threshold 0.8)
Hallucination      1.00   PASSED   (threshold 0.3)
```

**Why two providers?** A model grading its own homework is a conflict of interest. Groq answers, OpenRouter referees — an independent judge.

**How Groq works with the OpenAI SDK:** Groq exposes an OpenAI-compatible API, so the standard `openai` client is reused and only `base_url` changes:

```python
groq = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),      # a Groq "gsk_..." key
    base_url="https://api.groq.com/openai/v1",
)
```

---

## Getting started (per project)

```powershell
cd project_02

# 1. Create the venv
uv venv

# 2. Activate it
.venv\Scripts\activate

# 3. Install DeepEval
uv pip install deepeval

# 4. Configure your keys
copy .env.example .env        # then edit .env and paste real keys

# 5. Run an eval
deepeval test run test_02_Groq.py
```

> **Windows note:** `export VAR=value` is bash. In PowerShell use `$env:VAR = "value"`, but you usually don't need either — DeepEval auto-loads `.env`.

---

## Configuration

Providers are chosen with environment variables in each project's `.env` (gitignored). See the `.env.example` in each folder.

| Variable | Purpose |
|---|---|
| `USE_OPENROUTER_MODEL=true` | Make OpenRouter the active judge provider |
| `OPENROUTER_API_KEY=sk-or-...` | OpenRouter key |
| `OPENROUTER_MODEL_NAME=` | Optional judge model override |
| `USE_LOCAL_MODEL=true` | Opt into any OpenAI-compatible endpoint (Groq, vLLM, Ollama, LM Studio) |
| `LOCAL_MODEL_BASE_URL=` | e.g. `https://api.groq.com/openai/v1` |
| `LOCAL_MODEL_API_KEY=` | Key for that endpoint |
| `LOCAL_MODEL_NAME=` | Model id to call |

Without a `USE_*_MODEL` flag, DeepEval falls back to OpenAI and will demand `OPENAI_API_KEY`.

---

## Environment

| Tool | Version |
|---|---|
| OS | Windows (PowerShell) |
| uv | 0.12.3 |
| Python | 3.13 (uv-managed) |
| DeepEval | 4.2.x |

---

## Roadmap

- [x] Set up environment and first metric
- [x] Answer Relevancy + Hallucination metrics
- [x] Two-provider setup (Groq under test, OpenRouter judging)
- [ ] `GEval` custom criteria
- [ ] Datasets and batch evaluation
- [ ] Faithfulness / RAG metrics with real retrieval context
- [ ] Tracing and agent evaluation
- [ ] Confident AI cloud dashboard (optional)

---

## Security note

API keys live only in `.env`, which is gitignored. Only `.env.example` (with placeholders) is committed. If you clone this repo, bring your own keys.

---

## Links

- DeepEval docs — <https://deepeval.com/docs/getting-started>
- DeepEval repo — <https://github.com/confident-ai/deepeval>
- Groq console — <https://console.groq.com>
- OpenRouter models — <https://openrouter.ai/models>
