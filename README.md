# deepeval-learning

A hands-on learning repo for **[DeepEval](https://github.com/confident-ai/deepeval)** — an open-source, pytest-native framework for evaluating LLM applications.

The goal here isn't a product. It's a public log of me learning how to *measure* LLM output instead of eyeballing it: LLM-as-a-judge metrics, test cases, thresholds, and multi-provider setups.

---

## What's in here

| Project | Focus | Status |
|---|---|---|
| [`project_01/`](./project_01) | First setup: create a `uv` venv, install DeepEval, wire up a provider, write a first eval test | ✅ Working |
| [`project_02/`](./project_02) | Real evals: Answer Relevancy + Hallucination metrics, and grading a model served by **Groq** with a judge on **OpenRouter** | ✅ Working |
| [`project_03/`](./project_03) | Full setup: two live apps to test (a chatbot and a RAG pipeline) plus a DeepEval framework that scores them | 🚧 In progress |

Each project is self-contained with its own `.venv/`, `.env`, and README. `project_03` contains three sub-projects under one chapter folder.

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

### `project_03` — end-to-end: real apps under test

Everything so far evaluated a toy question ("what is 2+2?"). This project
scales it up: **real applications** with real system prompts, plus a framework
that scores them.

Three sub-projects under `chapter_16_DeepEval_Framwork/`:

| Sub-project | What it is | Port |
|---|---|---|
| `01_Chatbot_Shopeasy_chatbot/` | **Subsystem A** — ShopSphere support chatbot. FastAPI + React (Vite) + Groq, with a fixed support system prompt | 8201 (API), 5173 (UI) |
| `02_RAG_Explorer/` | **Subsystem B** — a RAG pipeline exposing every stage: ingest → chunk → embed (Nomic via Ollama) → store (ChromaDB) → retrieve → answer (Groq) | 8202 |
| `03_DeepFramework/` | **Subsystem C** — the DeepEval framework that scores A and B: 25 metric cards, pytest suite, and a dashboard | 8203 |

The whole point of running **live apps** rather than in-process functions is
that the eval exercises the same HTTP path a user would: the framework calls
`POST /chat` over the network, so a broken prompt, a broken proxy, or a broken
model selection all show up as a failing eval.

**Two models, deliberately different families:**

| Role | Model | Why |
|---|---|---|
| Under test | `qwen/qwen3.8-27b` | what the chatbot answers with |
| Judge | `openai/gpt-oss-120b` | scores every metric |

A judge grading its own sibling inflates scores through self-preference bias —
the same reason `project_02` split Groq and OpenRouter.

**Verified working** — both apps run and answer live.

`01_chatbot` (live mode through the Vite proxy):

```
Q: What is your refund policy?
A: ShopSphere processes refunds within 7 business days of receiving the
   returned item. Refunds are issued to your original payment method. ...

Q: How long does standard shipping take?
A: Standard shipping takes 5-7 business days inside the US.
   It is free on orders over $50.
```

`02_RAG_Explorer` (21 chunks seeded, retrieval → Groq with citations):

```
Q: How long does standard shipping take and what does it cost?
A: Standard domestic shipping takes 5-7 business days. The cost is free
   for orders over $50, otherwise it is $4.99 [shipping_policy.md #0].

Retrieved 4 hits — the chunk holding the answer ranked 2nd (0.67),
behind an international-shipping chunk (0.70)
mode: live · model: qwen/qwen3.8-27b
```

That second-place ranking is not a bug to fix — it is the kind of retrieval
imperfection `tests/rag/test_01_rag_contextual_precision.py` exists to score.

**Setup issues that cost real time** (documented in each sub-project's README):

1. **`groq==0.11.0` crashes on httpx 0.28+** (`01_chatbot`) — it passes a
   `proxies=` argument httpx removed. The client is built *outside* the
   `try/except` in `app.py`, so it surfaced as an opaque 500 instead of a clear
   error. Upgraded to `groq 1.7.0`. **Note:** the same pin works fine in
   `02_RAG_Explorer`, because ChromaDB pins `httpx==0.27.2` — pins are not
   portable between these two projects.
2. **`app.py` reads `os.getenv` but nothing loads `.env`** (both apps) —
   FastAPI does not auto-load it, and there is no `load_dotenv()` in either
   project. Needs an explicit `uvicorn --env-file .env`, or the app silently
   runs in **mock mode**.
3. **`npm install` skips Vite when `NODE_ENV=production`** (`01_chatbot`) —
   devDependencies get omitted. Needs `npm install --include=dev`.
4. **ChromaDB will not install on Python 3.13** (`02_RAG_Explorer`) — its
   `chroma-hnswlib` dependency has no cp313 wheel and tries to compile C++
   (`Microsoft Visual C++ 14.0 or greater is required`). Build the venv on
   **Python 3.11** instead.
5. **Ollama is a separate service** (`02_RAG_Explorer`) — the app never starts
   it. Nothing works without `ollama pull nomic-embed-text` and a running
   server on `:11434`; ingest fails with a 500.

**Scoring direction changed in DeepEval 4.x:** every metric is now
`score >= threshold`, so 1.0 is always a pass and `threshold` is always a
minimum. That includes Bias, Toxicity and PII Leakage, which scored the
opposite way in 3.x — a **high bias score means clean, not biased**. Most
tutorials and screenshots online are out of date on this.

---

## Getting started (per project)

`project_01` / `project_02` — pure DeepEval, no app to run:

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

`project_03` — start the apps under test first, then the framework. Full
instructions live in each sub-project's README
([chatbot](./project_03/chapter_16_DeepEval_Framwork/01_Chatbot_Shopeasy_chatbot/01_chatbot/README.md),
[RAG Explorer](./project_03/chapter_16_DeepEval_Framwork/02_RAG_Explorer/02_rag_explorer/README.md)):

```powershell
# Terminal 1 — the chatbot under test (Subsystem A)
cd project_03/chapter_16_DeepEval_Framwork/01_Chatbot_Shopeasy_chatbot/01_chatbot/backend
uv venv .venv --python 3.13
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload --port 8201 --env-file ..\.env

# Terminal 2 — the UI
cd ..\frontend
npm install --include=dev
npm run dev
```

Open <http://localhost:5173>. A **live** vs **mock** badge in the header tells
you whether the Groq key actually reached the backend.

```powershell
# Terminal 3 — the RAG Explorer (Subsystem B). Python 3.11, not 3.13.
cd project_03/chapter_16_DeepEval_Framwork/02_RAG_Explorer/02_rag_explorer
ollama pull nomic-embed-text          # once; needs a running Ollama
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --port 8202 --env-file .env

# seed the vector store once it is up (it starts empty)
curl -X POST "http://localhost:8202/api/ingest/seed?reset=true"
```

Open <http://localhost:8202>.

> **Windows note:** `export VAR=value` is bash. In PowerShell use
> `$env:VAR = "value"`. DeepEval auto-loads `.env`, but **FastAPI/uvicorn does
> not** — `project_03` needs an explicit `--env-file`.

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
| `GROQ_API_KEY=gsk_...` | Used by `project_03` apps for live answers |
| `CHATBOT_MODEL=qwen/qwen3.8-27b` | `project_03` model under test (defaults to `llama-3.3-70b-versatile`) |

Without a `USE_*_MODEL` flag, DeepEval falls back to OpenAI and will demand `OPENAI_API_KEY`.

---

## Environment

| Tool | Version |
|---|---|
| OS | Windows (PowerShell) |
| uv | 0.12.3 |
| Python | 3.13 (uv-managed) — **`02_RAG_Explorer` needs 3.11** for ChromaDB |
| Node.js / npm | 24.x / 11.x (for `project_03` frontend) |
| DeepEval | 4.2.x |
| FastAPI / uvicorn | 0.115 / 0.32 (`project_03`) |
| Ollama | latest, serving `nomic-embed-text` (`02_RAG_Explorer`) |
| groq SDK | 1.7.0 in `01_chatbot`; 0.11.0 in `02_RAG_Explorer` |

---

## Roadmap

- [x] Set up environment and first metric
- [x] Answer Relevancy + Hallucination metrics
- [x] Two-provider setup (Groq under test, OpenRouter judging)
- [x] Run evals against live apps over HTTP, not just in-process
- [x] Chatbot under test (Subsystem A) running live
- [x] RAG pipeline under test (Subsystem B) running with real retrieval
- [ ] Run the Subsystem C framework against both apps
- [ ] `GEval` custom criteria
- [ ] Datasets and batch evaluation
- [ ] Faithfulness / RAG metrics with real retrieval context
- [ ] Tracing and agent evaluation
- [ ] Confident AI cloud dashboard (optional)

---

## Security note

API keys live only in `.env`, which is gitignored. Only `.env.example` /
`.env.sample` (with placeholders) should be committed — if you clone this repo,
bring your own keys.

> **⚠️ Check before committing:** `.env.sample` files are *not* covered by the
> root `.gitignore` (which only matches `.env`, `.env.local`, `.env.*.local`).
> Confirm no real key has been pasted into one:
>
> ```powershell
> git ls-files | Select-String "\.env"
> git grep -n "gsk_\|sk-or-v1" -- "*.sample"
> ```

---

## Links

- DeepEval docs — <https://deepeval.com/docs/getting-started>
- DeepEval repo — <https://github.com/confident-ai/deepeval>
- Groq console — <https://console.groq.com>
- OpenRouter models — <https://openrouter.ai/models>
