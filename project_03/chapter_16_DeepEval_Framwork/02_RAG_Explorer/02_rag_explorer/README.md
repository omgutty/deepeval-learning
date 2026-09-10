# Subsystem B — RAG Explorer

A complete, locally-runnable RAG pipeline showcasing every stage:

```
ingest → chunk → embed (Nomic via Ollama) → store (ChromaDB) → retrieve → answer (Groq)
```

## Why "Explorer"

Most RAG demos hide retrieval behind the chat reply. This one **exposes every stage**: you see the raw chunks, the embeddings model, the retrieved hits with scores, and the grounded answer. That makes it auditable — exactly what DeepEval needs to evaluate retrieval, faithfulness, and grounding metrics.

## Port

`8202`

## Prerequisites

| Tool | Version used | Notes |
|---|---|---|
| **Python** | **3.11** | See gotcha 1 — 3.13 cannot install ChromaDB |
| Ollama | latest | embedding backend |
| `nomic-embed-text` | 274 MB | Ollama model |
| Groq API key | — | <https://console.groq.com/keys> |

## Configuration

Copy `.env.sample` to `.env` and fill in your keys:

```env
GROQ_API_KEY=gsk_...
RAG_MODEL=qwen/qwen3.8-27b
```

`RAG_MODEL` overrides `rag/chat.py`'s default (`llama-3.3-70b-versatile`) — set it
to a model your Groq key can actually access.

## Run (Windows / PowerShell)

Verified working on this machine.

```powershell
# 1. Ollama must be installed and running, with the embedding model pulled
winget install --id Ollama.Ollama --accept-package-agreements --accept-source-agreements
ollama pull nomic-embed-text

# 2. Python 3.11 venv (NOT 3.13 — see gotcha 1)
cd 02_rag_explorer
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe -r requirements.txt

# 3. Run (--env-file is required — see gotcha 2)
.\.venv\Scripts\python.exe -m uvicorn app:app --port 8202 --env-file .env
```

Open <http://localhost:8202>.

**4. Seed the corpus** (the store starts empty):

```powershell
curl -X POST "http://localhost:8202/api/ingest/seed?reset=true"
```

Expected:

```json
{"added":21,"documents":5,"stats":{"chunks":21,"sources":{
  "faq.md":6,"product_catalog.md":4,"refund_policy.md":3,
  "return_policy.md":4,"shipping_policy.md":4}}}
```

## Gotchas (and the fixes)

**1. ChromaDB will not install on Python 3.13.**

`chromadb==0.5.20` depends on `chroma-hnswlib`, which has no cp313 wheel and
falls back to compiling a C++ extension:

```
error: Microsoft Visual C++ 14.0 or greater is required.
```

Installing MSVC build tools is one fix; the simpler one is to build the venv on
**Python 3.11**, where prebuilt wheels exist:

```powershell
uv venv .venv --python 3.11
```

**2. `app.py` reads `os.getenv`, but nothing loads `.env`.**

There is no `load_dotenv()` anywhere in this project. FastAPI/uvicorn does not
auto-load `.env` either, so a plain `uvicorn app:app` runs with no key and the
chat falls back to **mock mode**. Pass the file explicitly:

```powershell
python -m uvicorn app:app --port 8202 --env-file .env
```

**3. `groq==0.11.0` happens to be fine *here*.** In the chatbot (Subsystem A)
the same pin breaks against httpx 0.28+. Here ChromaDB pins `httpx==0.27.2`,
which still accepts the `proxies` argument, so it works. Don't copy version
pins between the two projects without checking.

**4. Ollama is a separate service.** The app does not start it. If
`http://localhost:11434` is not answering, every ingest/search/chat call fails
at the embedding step (surfacing as a 500 on `/api/ingest/seed`).

## Pages

| Path | What |
|------|------|
| `/` | Pipeline dashboard (stage diagram, store stats) |
| `/ingest` | Seed bundled corpus, upload PDF/MD/TXT, view all chunks |
| `/search` | Pure retrieval — query goes through embeddings only, view ranked hits |
| `/chat` | Full RAG chat with the retrieval panel exposed below the reply |

## API

| Verb | Path | Body |
|------|------|------|
| GET | `/api/health` | — |
| POST | `/api/ingest/seed?reset=true|false` | — |
| POST | `/api/ingest/upload` | multipart `file` |
| POST | `/api/ingest/reset` | — |
| POST | `/api/search` | `{query, top_k}` |
| POST | `/api/chat` | `{message, top_k, history?}` |
| GET | `/api/chunks?source=…` | — |
| GET | `/api/stats` | — |

## Verified

Seeded 21 chunks, then a real query through retrieval → Groq:

```
Q: How long does standard shipping take and what does it cost?
A: Standard domestic shipping takes 5-7 business days. The cost is free
   for orders over $50, otherwise it is $4.99 [shipping_policy.md #0].

Retrieved 4 hits:
  shipping_policy.md #1   0.6975
  shipping_policy.md #0   0.6701   <- the chunk with the actual answer
  shipping_policy.md #2   0.6668
  return_policy.md   #2   0.5882

mode: live · model: qwen/qwen3.8-27b · 642 prompt / 38 completion tokens
```

Note the ranking: the chunk containing the answer (`#0`, with the cost and
delivery table) came back **second**, behind an international-shipping chunk.
That is exactly the failure mode `tests/rag/test_01_rag_contextual_precision.py`
from Subsystem C is built to catch — a useful signal that the metric has
something real to measure.

## What is in the bundled corpus

5 e-commerce knowledge files in `data/ecommerce/`:

- `refund_policy.md`
- `shipping_policy.md`
- `return_policy.md`
- `product_catalog.md`
- `faq.md`

These are intentionally rich enough to stress-test retrieval, faithfulness, and hallucination metrics from Subsystem C.
