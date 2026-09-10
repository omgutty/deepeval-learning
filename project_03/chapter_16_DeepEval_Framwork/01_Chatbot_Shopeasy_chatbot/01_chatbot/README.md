# Subsystem A — ShopSphere E-commerce Chatbot

React (Vite) frontend + FastAPI backend + Groq LLM. The "app under test" for the DeepEval framework.

The backend answers support questions (refunds, shipping, returns, accounts,
products) using a fixed system prompt. If no Groq key is configured it falls
back to a **mock mode** so the app still runs offline.

## Ports

| Service | Port |
|---|---|
| FastAPI backend | 8201 |
| Vite dev server | 5173 |

## Prerequisites

| Tool | Version used |
|---|---|
| Python | 3.13 |
| Node.js | 24.x |
| npm | 11.x |
| Groq API key | <https://console.groq.com/keys> |

## Configuration

Copy `.env.sample` to `.env` and fill in your keys:

```env
GROQ_API_KEY=gsk_...
CHATBOT_MODEL=qwen/qwen3.8-27b
```

`CHATBOT_MODEL` overrides the built-in default (`llama-3.3-70b-versatile`) —
set it to a model your key can actually access. See the full list with:

```powershell
# from backend/, with the venv active
python -c "from groq import Groq; import os; print([m.id for m in Groq(api_key=os.environ['GROQ_API_KEY']).models.list().data])"
```

## Run (Windows / PowerShell)

Verified working on this machine.

```powershell
# Terminal 1 — backend
cd backend
uv venv .venv --python 3.13
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload --port 8201 --env-file ..\.env

# Terminal 2 — frontend
cd frontend
npm install --include=dev
npm run dev
```

Open <http://localhost:5173>.

Expected health check:

```powershell
curl http://localhost:8201/health
# {"status":"ok","model":"qwen/qwen3.8-27b","groq_configured":true}
```

If `mode` comes back `"mock"` instead of `"live"`, the key did not reach the
process — see gotcha 2 below.

## Gotchas (and the fixes)

Three things blocked a straight copy-paste of the original instructions.

**1. `groq==0.11.0` is broken on httpx 0.28+.**

The pinned SDK passes a `proxies=` argument that httpx 0.28 removed, so the
client dies the moment it is constructed:

```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

Because `Groq(...)` is built *outside* the `try/except` in `app.py`, this
surfaces as an opaque `500 Internal Server Error` on every `/chat` call, not
a clean error message. Fix — upgrade the SDK:

```powershell
uv pip install -U groq      # 0.11.0 -> 1.7.0 (also bumps pydantic)
```

Worth updating `requirements.txt` so the pin stops biting.

**2. `app.py` reads `os.getenv`, but nothing loads `.env`.**

Unlike DeepEval, FastAPI does not auto-load a `.env` file, and `app.py` does
not call `load_dotenv()`. Running plain `uvicorn app:app` silently starts in
**mock mode**. Pass the file explicitly:

```powershell
python -m uvicorn app:app --port 8201 --env-file ..\.env
```

**3. `npm install` skips Vite when `NODE_ENV=production`.**

If the environment sets `NODE_ENV=production` (or npm config `omit=dev`),
devDependencies are skipped and `vite` never lands in `node_modules`:

```
'vite' is not recognized as an internal or external command
```

Force them in:

```powershell
npm install --include=dev
```

## API

| Verb | Path | Body / Notes |
|---|---|---|
| GET | `/health` | status + active model + whether Groq is configured |
| POST | `/chat` | `{message, history?}` → `{reply, model, mode, usage}` |

`mode` is `"live"` or `"mock"`. `usage` reports `prompt_tokens` and
`completion_tokens` so the DeepEval harness can bill the answer separately
from the tokens its judge spends scoring it.

## Verified

Both servers up, `qwen/qwen3.8-27b` answering in live mode through the Vite
proxy:

```
Q: What is your refund policy?
A: ShopSphere processes refunds within 7 business days of receiving the
   returned item. Refunds are issued to your original payment method. ...

Q: How long does standard shipping take?
A: Standard shipping takes 5-7 business days inside the US.
   It is free on orders over $50.
```

## Security

`.env` is gitignored and must never be committed. **`.env.sample` currently
contains real keys** — replace them with placeholders before committing, since
the root `.gitignore` only covers `.env`, `.env.local` and `.env.*.local`.
